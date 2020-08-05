from resources.identify_action import IdentifyAction
import concurrent.futures


class Parser:
    def start(list_of_access_logs, verbose):
        '''
        Accepts list[list_of_access_logs] where each item is a full path to an access log.
        Returns dict{all_parsed_logs} and dict{system_stats}
        '''
        executor = concurrent.futures.ProcessPoolExecutor()
        tasks = []  # storing individual thread details
        all_parsed_logs = []  # all dictionaries that will be compiled later

        for log in list_of_access_logs:
            # start new thread for each log file
            tasks.append(executor.submit(Parser.parse_log, log, verbose))
        for thread in concurrent.futures.as_completed(tasks):
            '''
            Each thread.result() will contain a dictionary where there will be 24 keys with each key
            containing a list of result sets. Each key will will be a date/hour timestamp for graphing purposes
            {"YYYY-MM-DD HH": [parsed_file, file_statistics], "YYYY-MM-DD HH+1": [parsed_file, file_statistics], ...}
            '''
            all_parsed_logs.append(thread.result())
        return Parser.compile_results(all_parsed_logs)

    def parse_log(path_to_access_log, verbose):
        '''
        Accepts a single path to a log file
        Returns dict{file_summarized} **time sensitive** and dict{file_statistics} **time insensitive**
        '''
        file_parsed = {}
        default_repo = {"clone": 0, "clone_miss": 0, "shallow": 0, "shallow_miss": 0,
                        "fetch": 0, "refs": 0, "refs_miss": 0, "push": 0, "unclassified": 0}
        file_statistics = {"repo_stats": {}, "operations": {"git_http": 0, "git_ssh": 0, "rest": 0, "web_ui": 0, "filesystem": 0}}
#        output_line_indicators = ['o@', 'o*']
        with open(path_to_access_log, 'r') as log:
            for line in log:
                split = line.split(' | ')
                try:
                    if ("o@" in split[2] and len(split) > 12) or ("o*" in split[2] and len(split) > 12):
                        protocol, request_id, timestamp, action, status_code, labels = Parser.parse_raw_line(split)
                        day, hour = Parser.parse_timestamp(timestamp)
                        parsed_action = IdentifyAction.parse(protocol, request_id, action, status_code, labels, verbose)

                        if day not in file_parsed.keys():
                            # add dict for day as place holder
                            file_parsed[day] = {}
                        else:
                            if hour not in file_parsed[day].keys():
                                # add hour within day with a list, with the first value = parsed_action
                                file_parsed[day][hour] = [parsed_action]
                            else:
                                # concatenate the existing values for that hour with this line
                                file_parsed[day][hour].append(parsed_action)

                        repo_identifier = Parser.identify_repo(parsed_action, action)
                        if repo_identifier is None:
                            pass
                        else:
                            # if repo doesn't yet exist, initialize it
                            if parsed_action['op_action'] != "" and parsed_action['op_action'] != "ignore":
                                if repo_identifier not in file_statistics['repo_stats'].keys():
                                    file_statistics['repo_stats'][repo_identifier] = default_repo.copy()
                                file_statistics['repo_stats'][repo_identifier][parsed_action['op_action']] += 1

                        # file_statistics['operations'] increments
                        if parsed_action['git_type'] == "http":
                            file_statistics['operations']['git_http'] += 1
                        elif parsed_action['git_type'] == "ssh":
                            file_statistics['operations']['git_ssh'] += 1
                        elif parsed_action['op_action'] == 'rest':
                            file_statistics['operations']['rest'] += 1
                        elif parsed_action['op_action'] == 'web_ui':
                            file_statistics['operations']['web_ui'] += 1
                        elif parsed_action['op_action'] == 'filesystem':
                            file_statistics['operations']['filesystem'] += 1

                except IndexError:
                    pass # Drop incomplete lines and lines that don't match our search criteria

        file_summarized = Parser.merge_hours(file_parsed)
        return file_summarized, file_statistics

    def parse_raw_line(split):
        '''
        Parsed based on access log format:
        https://confluence.atlassian.com/bitbucketserverkb/how-to-read-the-bitbucket-server-log-formats-779171668.html
        '''
#        ip_address = split[0]  # not used
        protocol = split[1]
        request_id = split[2]
        timestamp = split[4]
        action = split[5]
#        request_details = split[6]  # not used
        status_code = split[7]
        labels = split[10]
        return protocol, request_id, timestamp, action, status_code, labels

    def identify_repo(parsed_action, action):

        # file_statistics['repo_stats'] increments
        '''
        Identify the repo, requires str(action)
        Examples:
            HTTP: "POST /scm/project_key/repo_slug.git/git-upload-pack HTTP/1.1"
            SSH: SSH - git-upload-pack '/project_key/repo_slug.git'
        '''
        repo_identifier = None
        if parsed_action['git_type'] == "http":
            # look for the repo after the POST/GET and trim unnecessary info
            temp = action.split("/scm/")[1].split("/")
            repo_identifier = str.join("/", (temp[0], temp[1])).split(".git")[0].strip("'").lower()
        elif parsed_action['git_type'] == "ssh":
            # look for the repo within single quotes and strip off the trailing ".git'"
            temp = action.split("'/")[1].split("/")
            repo_identifier = str.join("/", (temp[0], temp[1])).split(".git")[0].strip("'").lower()
        else:
            pass  # Not a git operation
        return repo_identifier

    def parse_timestamp(timestamp):
        # From: "2020-04-27 14:21:23,359" To: "2020-04-27 14"
        '''
        Accepts: string("YYYY-MM-DD HH:MM:SS,SSS)
        Returns: 2 objects, int(day) and int(hour)
            "day" = 7 digit int, YYYYMMDD
            "hour" = 2 digit int, HH
        '''
        split = timestamp.split(' ')
        day_temp = split[0].replace('-', '')
        day = int(day_temp)
        hour_temp = split[1].split(':')[0]
        hour = int(hour_temp)
        return day, hour

    def merge_hours(file_parsed):
        '''
        Accepts dict{file_parsed}
        Returns dict{parsed_log}
        '''
        file_summarized = {}
        default = { "total_clones": 0,
                    "total_clone_misses": 0,
                    "total_shallow_clones": 0,
                    "total_shallow_clone_misses": 0,
                    "total_fetches": 0,
                    "total_ref_ads": 0,
                    "total_ref_ad_misses": 0,
                    "total_pushes": 0,
                    "total_rest_calls": 0,
                    "total_filesystem_calls": 0,
                    "total_webui_calls": 0,
                    "total_git_ssh_operations": 0,
                    "total_git_http_operations": 0,
                    "highest_seen_concurrent_operations": 0,
                    "total_unclassified": 0
                    }

        for day in file_parsed:
            if day not in file_summarized.keys():
                file_summarized[day] = {}
            for hour in file_parsed[day]:
                if hour not in file_summarized[day].keys():
                    file_summarized[day][hour] = default.copy()
                for action in file_parsed[day][hour]:
                    if action['op_action'] == "clone": file_summarized[day][hour]['total_clones'] += 1
                    elif action['op_action'] == "clone_miss": file_summarized[day][hour]['total_clone_misses'] += 1
                    elif action['op_action'] == "shallow": file_summarized[day][hour]['total_shallow_clones'] += 1
                    elif action['op_action'] == "shallow_miss": file_summarized[day][hour]['total_shallow_clone_misses'] += 1
                    elif action['op_action'] == "fetch": file_summarized[day][hour]['total_fetches'] += 1
                    elif action['op_action'] == "refs": file_summarized[day][hour]['total_ref_ads'] += 1
                    elif action['op_action'] == "refs_miss": file_summarized[day][hour]['total_ref_ad_misses'] += 1
                    elif action['op_action'] == "push": file_summarized[day][hour]['total_pushes'] += 1
                    elif action['op_action'] == "rest": file_summarized[day][hour]['total_rest_calls'] += 1
                    elif action['op_action'] == "filesystem": file_summarized[day][hour]['total_filesystem_calls'] += 1
                    elif action['op_action'] == "web_ui": file_summarized[day][hour]['total_webui_calls'] += 1
                    elif action['op_action'] == "unclassified": file_summarized[day][hour]['total_unclassified'] += 1

                    if action['git_type'] == "ssh": file_summarized[day][hour]['total_git_ssh_operations'] += 1
                    elif action['git_type'] == "http": file_summarized[day][hour]['total_git_http_operations'] += 1

                    if action['max_connections'] > file_summarized[day][hour]['highest_seen_concurrent_operations']:
                        file_summarized[day][hour]['highest_seen_concurrent_operations'] = action['max_connections']
        return(file_summarized)

    def compile_results(all_logs):
        '''
        Accepts list[all_logs] where each item is a list containing [file_parsed, file_statistics] from parse_log()
        Returns dict{all_days} & dict{log_stats}
        '''
        all_days = {}
        all_repo_stats = {}
        default_hour = { "total_clones": 0,
                         "total_clone_misses": 0,
                         "total_shallow_clones": 0,
                         "total_shallow_clone_misses": 0,
                         "total_fetches": 0,
                         "total_ref_ads": 0,
                         "total_ref_ad_misses": 0,
                         "total_pushes": 0,
                         "total_rest_calls": 0,
                         "total_filesystem_calls": 0,
                         "total_webui_calls": 0,
                         "total_git_ssh_operations": 0,
                         "total_git_http_operations": 0,
                         "highest_seen_concurrent_operations": 0,
                         "total_unclassified": 0
                         }
        default_repo = { "total_clones": 0,
                         "total_clone_misses": 0,
                         "total_shallow_clones": 0,
                         "total_shallow_clone_misses": 0,
                         "total_fetches": 0,
                         "total_ref_ads": 0,
                         "total_ref_ad_misses": 0,
                         "total_pushes" : 0,
                         "total_unclassified": 0
                        }
        operations = { "git_http": 0,
                       "git_ssh": 0,
                       "rest": 0,
                       "web_ui": 0,
                       "filesystem": 0
                      }

        for log_result in all_logs:
            single_file_summarized = log_result[0]
            single_file_statistics = log_result[1]

            for day in single_file_summarized:  # maybe drop keys
                if day not in all_days.keys():
                    all_days[day] = {}
                for hour in single_file_summarized[day]:
                    if hour not in all_days[day].keys():
                        # initialize zero'd counters for hour
                        all_days[day][hour] = default_hour.copy()
                    
                    # already exists, update existing with current
                    all_days[day][hour]['total_clones'] += single_file_summarized[day][hour]['total_clones']
                    all_days[day][hour]['total_clone_misses'] += single_file_summarized[day][hour]['total_clone_misses']
                    all_days[day][hour]['total_shallow_clones'] += single_file_summarized[day][hour]['total_shallow_clones']
                    all_days[day][hour]['total_shallow_clone_misses'] += single_file_summarized[day][hour]['total_shallow_clone_misses']
                    all_days[day][hour]['total_fetches'] += single_file_summarized[day][hour]['total_fetches']
                    all_days[day][hour]['total_ref_ads'] += single_file_summarized[day][hour]['total_ref_ads']
                    all_days[day][hour]['total_ref_ad_misses'] += single_file_summarized[day][hour]['total_ref_ad_misses']
                    all_days[day][hour]['total_pushes'] += single_file_summarized[day][hour]['total_pushes']
                    all_days[day][hour]['total_rest_calls'] += single_file_summarized[day][hour]['total_rest_calls']
                    all_days[day][hour]['total_filesystem_calls'] += single_file_summarized[day][hour]['total_filesystem_calls']
                    all_days[day][hour]['total_webui_calls'] += single_file_summarized[day][hour]['total_webui_calls']
                    all_days[day][hour]['total_git_ssh_operations'] += single_file_summarized[day][hour]['total_git_ssh_operations']
                    all_days[day][hour]['total_git_http_operations'] += single_file_summarized[day][hour]['total_git_http_operations']
                    all_days[day][hour]['total_unclassified'] += single_file_summarized[day][hour]['total_unclassified']
                    if single_file_summarized[day][hour]['highest_seen_concurrent_operations'] > all_days[day][hour]['highest_seen_concurrent_operations']:
                        all_days[day][hour]['highest_seen_concurrent_operations'] = single_file_summarized[day][hour]['highest_seen_concurrent_operations']

            # Compile all_repo_stats
            for repo_identifier in single_file_statistics['repo_stats']:
                if repo_identifier not in all_repo_stats.keys():
                    # If the repo doesn't yet exist, initialize it
                    all_repo_stats[repo_identifier] = default_repo.copy()
                all_repo_stats[repo_identifier]['total_clones'] += single_file_statistics['repo_stats'][repo_identifier]['clone']
                all_repo_stats[repo_identifier]['total_clone_misses'] += single_file_statistics['repo_stats'][repo_identifier]['clone_miss']
                all_repo_stats[repo_identifier]['total_shallow_clones'] += single_file_statistics['repo_stats'][repo_identifier]['shallow']
                all_repo_stats[repo_identifier]['total_shallow_clone_misses'] += single_file_statistics['repo_stats'][repo_identifier]['shallow_miss']
                all_repo_stats[repo_identifier]['total_fetches'] += single_file_statistics['repo_stats'][repo_identifier]['fetch']
                all_repo_stats[repo_identifier]['total_ref_ads'] += single_file_statistics['repo_stats'][repo_identifier]['refs']
                all_repo_stats[repo_identifier]['total_ref_ad_misses'] += single_file_statistics['repo_stats'][repo_identifier]['refs_miss']
                all_repo_stats[repo_identifier]['total_pushes'] += single_file_statistics['repo_stats'][repo_identifier]['push']
                all_repo_stats[repo_identifier]['total_unclassified'] += single_file_statistics['repo_stats'][repo_identifier]['unclassified']

            # Compile Operations stats
            operations['git_http'] += single_file_statistics['operations']['git_http']
            operations['git_ssh'] += single_file_statistics['operations']['git_ssh']
            operations['rest'] += single_file_statistics['operations']['rest']
            operations['web_ui'] += single_file_statistics['operations']['web_ui']
            operations['filesystem'] += single_file_statistics['operations']['filesystem']

        log_stats = {'repo_stats': all_repo_stats, 'operations': operations}
        return all_days, log_stats
