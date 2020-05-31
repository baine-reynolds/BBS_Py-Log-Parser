import concurrent.futures
import re

class Parser:
    def start(list_of_access_logs):
        '''
        Accepts list[list_of_access_logs] where each item is a full path to an access log.
        Returns dict{all_parsed_logs} and dict{system_stats}

            dict{all_parsed_logs}
            { "YYYY-MM-DD HH": { "total_clones" = int(counter, default = 0),
                                 "total_clone_misses" = int(counter, default = 0),
                                 "total_shallow_clones" = int(counter, default = 0),
                                 "total_shallow_clone_misses" = int(counter, default = 0),
                                 "total_fetches" = int(counter, default = 0),
                                 "total_fetch_misses" = int(counter, default = 0),
                                 "total_ref_ads" = int(counter, default = 0),
                                 "total_ref_ad_miss" = int(counter, default = 0),
                                 "total_pushes" = int(counter, default = 0),
                                 "total_rest_calls" = int(counter, default = 0),
                                 "total_filesystem_calls" = int(counter, default = 0),
                                 "total_webui_calls" = int(counter, default = 0),
                                 "total_git_ssh_operations" = int(counter, default = 0),
                                 "total_git_http_operations" = int(counter, default = 0),
                                 "highest_seen_concurrent_operations" = int(counter, default = 0)
                                },
            "YYYY-MM-DD HH": { "total_clones" = int(counter, default = 0),
                               "total_clone_misses" = int(counter, default = 0),
                               "total_shallow_clones" = int(counter, default = 0),
                               "total_shallow_clone_misses" = int(counter, default = 0),
                               "total_fetches" = int(counter, default = 0),
                               "total_fetch_misses" = int(counter, default = 0),
                               "total_ref_ads" = int(counter, default = 0),
                               "total_ref_ad_miss" = int(counter, default = 0),
                               "total_pushes" = int(counter, default = 0),
                               "total_rest_calls" = int(counter, default = 0),
                               "total_filesystem_calls" = int(counter, default = 0),
                               "total_webui_calls" = int(counter, default = 0),
                               "total_git_ssh_operations" = int(counter, default = 0),
                               "total_git_http_operations" = int(counter, default = 0),
                               "highest_seen_concurrent_operations" = int(counter, default = 0)
                             },
            ...
            },
            dict{system_stats}
            {"repo_stats": { repo_identifier: { "total_clones" = int(counter, default = 0),
                                                "total_clone_misses" = int(counter, default = 0),
                                                "total_shallow_clones" = int(counter, default = 0),
                                                "total_shallow_clone_misses" = int(counter, default = 0),
                                                "total_fetches" = int(counter, default = 0),
                                                "total_fetch_misses" = int(counter, default = 0),
                                                "total_ref_ads" = int(counter, default = 0),
                                                "total_ref_ad_miss" = int(counter, default = 0),
                                                "total_pushes" = int(counter, default = 0)
                                               },
                             repo_identifier: { "total_clones" = int(counter, default = 0),
                                                "total_clone_misses" = int(counter, default = 0),
                                                "total_shallow_clones" = int(counter, default = 0),
                                                "total_shallow_clone_misses" = int(counter, default = 0),
                                                "total_fetches" = int(counter, default = 0),
                                                "total_fetch_misses" = int(counter, default = 0),
                                                "total_ref_ads" = int(counter, default = 0),
                                                "total_ref_ad_miss" = int(counter, default = 0),
                                                "total_pushes" = int(counter, default = 0)
                                               },
                             ...
                            } 
             "operations": { "git_http": call_counter,
                             "git_ssh": call_counter,
                             "rest": call_counter,
                             "web_ui": call_counter,
                             "file_system": call_counter
            }
        '''
        executor = concurrent.futures.ThreadPoolExecutor()
        tasks = []  # storing individual thread details
        all_parsed_logs = []  # all dictionaries that will be compiled later

        for log in list_of_access_logs:
            # start new thread for each log file
            tasks.append(executor.submit(Parser.parse_log, log))
        for thread in concurrent.futures.as_completed(tasks):
            '''
            Each thread.result() will contain a dictionary where there will be 24 keys with each key
            containing a list of result sets. Each key will will be a date/hour timestamp for graphing purposes
            {"YYYY-MM-DD HH": [parsed_file, file_statistics], "YYYY-MM-DD HH+1": [parsed_file, file_statistics], ...}

            '''
            all_parsed_logs.append(thread.result())
        return Parser.compile_results(all_parsed_logs)

    def parse_log(path_to_access_log):
        '''
        Accepts a single path to a log file
        Returns dict{file_summarized} **time sensitive** and dict{file_statistics} **time insensitive** where:
            file_summarized is a dict containing a summary of operations within each hour in the log
                { "YYYY-MM-DD HH": { "total_clones" = int(counter, default = 0),
                                 "total_clone_misses" = int(counter, default = 0),
                                 "total_shallow_clones" = int(counter, default = 0),
                                 "total_shallow_clone_misses" = int(counter, default = 0),
                                 "total_fetches" = int(counter, default = 0),
                                 "total_fetch_misses" = int(counter, default = 0),
                                 "total_ref_ads" = int(counter, default = 0),
                                 "total_ref_ad_miss" = int(counter, default = 0),
                                 "total_pushes" = int(counter, default = 0),
                                 "total_rest_calls" = int(counter, default = 0),
                                 "total_filesystem_calls" = int(counter, default = 0),
                                 "total_webui_calls" = int(counter, default = 0),
                                 "total_git_ssh_operations" = int(counter, default = 0),
                                 "total_git_http_operations" = int(counter, default = 0),
                                 "highest_seen_concurrent_operations" = int(counter, default = 0)
                                    },
                  ...
                }
            file_statistics is a dict containing "repo_stats" and "operations"
                { "repo_stats": { repo_identifier: { "total_clones" = int(counter, default = 0),
                                                     "total_clone_misses" = int(counter, default = 0),
                                                     "total_shallow_clones" = int(counter, default = 0),
                                                     "total_shallow_clone_misses" = int(counter, default = 0),
                                                     "total_fetches" = int(counter, default = 0),
                                                     "total_fetch_misses" = int(counter, default = 0),
                                                     "total_ref_ads" = int(counter, default = 0),
                                                     "total_ref_ad_miss" = int(counter, default = 0),
                                                     "total_pushes" = int(counter, default = 0)
                                                  },
                                repo_identifier: { "total_clones" = int(counter, default = 0),
                                                   "total_clone_misses" = int(counter, default = 0),
                                                   "total_shallow_clones" = int(counter, default = 0),
                                                   "total_shallow_clone_misses" = int(counter, default = 0),
                                                   "total_fetches" = int(counter, default = 0),
                                                   "total_fetch_misses" = int(counter, default = 0),
                                                   "total_ref_ads" = int(counter, default = 0),
                                                   "total_ref_ad_miss" = int(counter, default = 0),
                                                   "total_pushes" = int(counter, default = 0)
                                                  },
                                ...
                                },
                "operations": { "git_http": call_counter,
                                "git_ssh": call_counter,
                                "rest": call_counter,
                                "web_ui": call_counter,
                                "file_system": call_counter
                                ### potentially add "lfs" here
                              }
                }
        '''
        file_parsed = {}
        file_statistics = {"repo_stats": {}, "operations": {"git_http": 0, "git_ssh": 0, "rest": 0, "web_ui": 0, "filesystem": 0}}
        output_line_indicators = ['o@', 'o*']
        with open(path_to_access_log, 'r') as log:
            for line in log:
                split = line.split(' | ')
                if output_line_indicators in split[3] and len(split) > 12:
                    '''
                    Parsed based on access log format:
                    https://confluence.atlassian.com/bitbucketserverkb/how-to-read-the-bitbucket-server-log-formats-779171668.html
                    '''
                    #ip_address = split[0]  # not used
                    protocol = split[1]
                    request_id = split[2]
                    timestamp = split[4]
                    action = split[5]
                    #request_details = split[6]  # not used
                    status_code = split[7]
                    git_op = split[10]

                    parsed_timestamp = timestamp.split(':')[0]  # From: "2020-04-27 14:21:23,359" To: "2020-04-27 14"
                    parsed_action = Parser.identify_action(protocol, request_id, action, status_code, git_op)

                    if file_parsed[parsed_timestamp]:
                        # concatenate the existing values for that hour with this line
                        file_parsed[parsed_timestamp] = file_parsed[parsed_timestamp].append(parsed_action)
                    else:
                        file_parsed[parsed_timestamp] = [parsed_action]

                    # file_statistics['repo_stats'] increments
                    '''
                    Identify the repo, requires str(action)
                    Examples:
                        HTTP: "POST /scm/project_key/repo_slug.git/git-upload-pack HTTP/1.1"
                        SSH: SSH - git-upload-pack '/project_key/repo_slug.git'
                    '''
                    repo_identifier = None
                    if parsed_action['git_op'] == "http":
                        # look for the repo after the POST/GET and trim unnecessary info
                        repo_identifier = action.split(' ')[1].split(".git")[0].strip("/scm")
                    elif parsed_action['git_op'] == "ssh":
                        # look for the repo within single quotes and strip off the trailing ".git'"
                        repo_identifier = action.split("'")[1].split(".git")[0]
                    else:
                        print(f"Couldn't properly parse '{action}' for a project/repo key/slug")

                    if repo_identifier == None:
                        pass
                    else:
                        if file_statistics['repo_stats'][repo_identifier]:
                            # repo already exists, update the appropreiate counter
                            file_statistics['repo_stats'][repo_identifier][parsed_action['op_action']] += 1
                        else:
                            # initialize the empty repo and then increment the relevant counter
                            file_statistics['repo_stats'][repo_identifier] = {"clone": 0,
                                                                              "clone_miss": 0,
                                                                              "shallow": 0,
                                                                              "shallow_miss": 0,
                                                                              "fetch": 0,
                                                                              "fetch_miss": 0,
                                                                              "refs": 0,
                                                                              "refs_miss": 0,
                                                                              "push": 0
                                                                             }
                            file_statistics['repo_stats'][repo_identifier][parsed_action['op_action']] += 1

                    # file_statistics['operations'] increments
                    if parsed_action['git_op'] == "http":
                        file_statistics['operations']['git_http'] += 1
                    elif parsed_action['git_op'] == "ssh":
                        file_statistics['operations']['git_ssh'] += 1
                    elif parsed_action['op_action'] == 'rest':
                        file_statistics['operations']['rest'] += 1
                    elif parsed_action['op_action'] == 'web_ui':
                        file_statistics['operations']['web_ui'] += 1
                    elif parsed_action['op_action'] == 'filesystem':
                        file_statistics['operations']['filesystem'] += 1

                elif len(split) < 12:
                    pass # broken line that is commonly found as start/end of a file.
                    # Potentially worth counting for indication of issues but skipping for now.
                elif output_line_indicators not in split[3]:
                    pass # skip input lines as they provide minimal information
                else:
                    print(f"Could not match against the line:\n\t{line}\n")

        file_summarized = Parser.merge_hours(file_parsed)
        return file_summarized, file_statistics

    def identify_action(protocol, request_id, action, status_code, git_op):
        """
        Accepts the following access log fields:
            str(protocol),
            str(request_id),
            str(action),
            str(status_code),
            str(git_op)

        Returns a dict{identified_action} containing 2 key/value pairs:
            dict{identified_action}
            {"op_action": str(value),

                "value" must be one of the following strings:
                "clone", "clone_miss", "shallow", "shallow_miss",
                "fetch", "fetch_miss", "refs", "refs_miss",
                "push", "rest_api", "web_ui", "filesystem",
                "invalid" (default)
                default is only seen if the parsing failed to identify the action
            "max_connections": int(value)
            }
        """
        op_action = "invalid"
        git_op = ""

        concurrent_connections = int(request_id.split('x')[3])

        actions = action.split(' ')
        if "http" in str(protocol).lower():

            op_type = actions[2].lower  # ignoring get vs post vs delete for now

            if "/rest/api" in op_type:
                # rest api interaction
                op_action = "rest_api"
            elif "/rest/" in op_type:
                # internal REST like permissions
                op_action = "web_ui"
            elif "/scm/" in op_type:
                # git operation
                git_op = "http"
                if int(status_code) in range(200,299):
                    if "push" in git_op:
                        op_action = "push"
                    elif "clone" in git_op:
                        if "shallow" in git_op:
                            if "miss" in git_op:
                                op_action = "shallow_miss"
                            elif "hit" in git_op:
                                op_action = "shallow"
                            else:
                                print(f"Unknown state, skipping. Code 10000\n{git_op}")
                                op_action = "invalid"
                        else: # non-shallow
                            if "miss" in git_op:
                                op_action = "clone_miss"
                            elif "hit" in git_op:
                                op_action = "clone"
                            else:
                                print(f"Unknown state, skipping. Code 10001\n{git_op}")
                    elif "fetch" in git_op:
                        if "miss" in git_op:
                            op_action = "fetch_miss"
                        elif "hit" in git_op:
                            op_action = "fetch"
                        elif "bypass" in git_op:
                            # not sure   #############################################################
                            pass
                        else:
                            print(f"Unknown state, skipping. Code 10002\n{git_op}")
                    elif "refs" in git_op:
                        if "miss" in git_op:
                            op_action = "refs_miss"
                        elif "hit" in git_op:
                            op_action = "refs"
                        elif "bypass" in git_op:
                            # not sure   #############################################################
                            pass
                        else:
                            print("Unknown state, skipping. Code 10003")
                            pass
                    else:
                        print(f"Unknown state, skipping. Code 10004\n{git_op}")
                        pass
                else:
                    # parsing out initial auth requests as a single http git op takes 3 requests
                    pass
            elif "/plugins/servlet" in op_type:
                # internal features (includes webhooks, permissions, integrations)
                # not sure   #############################################################
                pass
            elif [x for x in ["/s/", "/download/"] if(x in op_type)]:
                # static file request from WebUI
                # /projects, /users, 
                op_action = "filesystem"
            elif [x for x in ["/admin/", "account", "/dashboard", "/mvc/"] if(x in op_type)]: 
                # any matches for the above list identifying WebUI interactions
                op_action = "web_ui"
            else:
                print(f"Cannot parse line, please update Parser.identify_action with appropreiate use case for:\n{op_type}")
        elif "ssh" in str(protocol).lower():
            git_op = "ssh"
            if "push" in git_op:
                op_action = "push"
            elif  "clone" in git_op:
                if "shallow" in git_op:
                    if "miss" in git_op:
                        op_action = "shallow_miss"
                    elif "hit" in git_op:
                        op_action = "shallow"
                    elif "bypass" in git_op:
                        # not sure   #############################################################
                        pass
                    else:
                        print(f"unknown state, skipping. Code 10005\n{git_op}")
                        pass
                if "miss" in git_op:
                    op_action = "clone_miss"
                elif "hit" in git_op:
                    op_action = "clone"
                elif "bypass" in git_op:
                    # not sure   #############################################################
                    pass
                else:
                    print(f"Unknown state, skipping. Code 10006\n{git_op}")
                    pass
            elif "fetch" in git_op:
                if "miss" in git_op:
                    op_action = "fetch_miss"
                elif "hit" in git_op:
                    op_action = "fetch"
                elif "bypass" in git_op:
                    # not sure   #############################################################
                    pass
                else:
                    print(f"Unknown state, skipping. Code 10007\n{git_op}")
                    pass
            elif "refs" in git_op:
                if "miss" in git_op:
                    op_action = "refs_miss"
                elif "hit" in git_op:
                    op_action = "refs"
                elif "bypass" in git_op:
                    # not sure   #############################################################
                    pass
                else:
                    print(f"Unknown state, skipping. Code 10008\n{git_op}")
        else:
            print(f"Could not parse protocol: '{protocol}' properly")
        identified_action = {"op_action": op_action, "git_op": git_op, "max_connections": concurrent_connections}
        return identified_action

    def merge_hours(file_parsed):
        '''
        Accepts dict{file_parsed}
            file_parsed is a dict who's keys are a str(parsed_timestamp) and values are a dict{parsed_action} from identify_action()
                {
                    "2020-05-17 01": [parsed_action1,
                                      parsed_action2,
                                      ...
                                      ]
                    "2020-05-17 02": [parsed_action1,
                                      parsed_action2,
                                      ...
                                      ]
                    "2020-05-17 03": [parsed_action1,
                                      parsed_action2,
                                      ...
                                      ]
                    ...
                }
        Returns dict{parsed_log}
            { "YYYY-MM-DD HH": { "total_clones" = int(counter, default = 0),
                                 "total_clone_misses" = int(counter, default = 0),
                                 "total_shallow_clones" = int(counter, default = 0),
                                 "total_shallow_clone_misses" = int(counter, default = 0),
                                 "total_fetches" = int(counter, default = 0),
                                 "total_fetch_misses" = int(counter, default = 0),
                                 "total_ref_ads" = int(counter, default = 0),
                                 "total_ref_ad_miss" = int(counter, default = 0),
                                 "total_pushes" = int(counter, default = 0),
                                 "total_rest_calls" = int(counter, default = 0),
                                 "total_filesystem_calls" = int(counter, default = 0),
                                 "total_webui_calls" = int(counter, default = 0),
                                 "total_git_ssh_operations" = int(counter, default = 0),
                                 "total_git_http_operations" = int(counter, default = 0),
                                 "highest_seen_concurrent_operations" = int(counter, default = 0)
                                },
                ...
            }
        '''
        file_summarized = {}
        default = { "total_clones": 0,
                    "total_clone_misses": 0,
                    "total_shallow_clones": 0,
                    "total_shallow_clone_misses": 0,
                    "total_fetches": 0,
                    "total_fetch_misses": 0,
                    "total_ref_ads": 0,
                    "total_ref_ad_miss": 0,
                    "total_pushes": 0,
                    "total_rest_calls": 0,
                    "total_filesystem_calls": 0,
                    "total_webui_calls": 0,
                    "total_git_ssh_operations": 0,
                    "total_git_http_operations": 0,
                    "highest_seen_concurrent_operations": 0 
                   }
        for timestamp, parsed_action_list in file_parsed:
            this_hour = {timestamp: default}
            for action in parsed_action_list:
                if action['op_action'] == "clone":
                    this_hour['total_clones'] += 1
                elif action['op_action'] == "clone_miss":
                    this_hour['total_clone_misses'] += 1
                elif action['op_action'] == "shallow":
                    this_hour['total_shallow_clones'] += 1
                elif action['op_action'] == "shallow_miss":
                    this_hour['total_shallow_clone_misses'] += 1
                elif action['op_action'] == "fetch":
                    this_hour['total_fetches'] += 1
                elif action['op_action'] == "fetch_miss":
                    this_hour['total_fetch_misses'] += 1
                elif action['op_action'] == "refs":
                    this_hour['total_ref_ads'] += 1
                elif action['op_action'] == "refs_miss":
                    this_hour['total_ref_ad_miss'] += 1
                elif action['op_action'] == "push":
                    this_hour['total_pushes'] += 1
                elif action['op_action'] == "rest_api":
                    this_hour['total_rest_calls'] += 1
                elif action['op_action'] == "filesystem":
                    this_hour['total_filesystem_calls'] += 1
                elif action['op_action'] == "web_ui":
                    this_hour['total_webui_calls'] += 1

                if action['git_op'] == "ssh":
                    this_hour['total_git_ssh_operations'] += 1
                elif action['git_op'] == "http":
                    this_hour['total_git_http_operations'] += 1

                if action['max_connections'] > this_hour['highest_seen_concurrent_operations']:
                    this_hour['highest_seen_concurrent_operations'] = action['max_connections']
            file_summarized[this_hour]
        return(file_summarized)

    def compile_results(all_logs):
        '''
        Accepts list[all_logs] where each item is a list containing [file_parsed, file_statistics] from parse_log()

        '''
        hour_breakdown = {}
        repo_stats = {}
        operations = {"git_http": 0,
                      "git_ssh": 0,
                      "rest": 0,
                      "web_ui": 0,
                      "file_system": 0
                      }

        for log_result in all_logs:
            file_summarized = log_result[0]
            file_statistics = log_result[1]

            # If timestamp exists in two logs, compile the results, else, append result set to dict{hour_breakdown}
            for timestamp, hour_summary in file_summarized:
                if hour_breakdown[timestamp]:
                    # already exists, update existing with current
                    hour_breakdown[timestamp]['total_clones'] += hour_summary['total_clones']
                    hour_breakdown[timestamp]['total_clone_misses'] += hour_summary['total_clone_misses']
                    hour_breakdown[timestamp]['total_shallow_clones'] += hour_summary['total_shallow_clones']
                    hour_breakdown[timestamp]['total_shallow_clone_misses'] += hour_summary['total_shallow_clone_misses']
                    hour_breakdown[timestamp]['total_fetches'] += hour_summary['total_fetches']
                    hour_breakdown[timestamp]['total_fetch_misses'] += hour_summary['total_fetch_misses']
                    hour_breakdown[timestamp]['total_ref_ads'] += hour_summary['total_ref_ads']
                    hour_breakdown[timestamp]['total_ref_ad_miss'] += hour_summary['total_ref_ad_miss']
                    hour_breakdown[timestamp]['total_pushes'] += hour_summary['total_pushes']
                    hour_breakdown[timestamp]['total_rest_calls'] += hour_summary['total_rest_calls']
                    hour_breakdown[timestamp]['total_filesystem_calls'] += hour_summary['total_filesystem_calls']
                    hour_breakdown[timestamp]['total_webui_calls'] += hour_summary['total_webui_calls']
                    hour_breakdown[timestamp]['total_git_ssh_operations'] += hour_summary['total_git_ssh_operations']
                    hour_breakdown[timestamp]['total_git_http_operations'] += hour_summary['total_git_http_operations']
                    if hour_summary['highest_seen_concurrent_operations'] > hour_breakdown[timestamp]['highest_seen_concurrent_operations']:
                        hour_breakdown[timestamp]['highest_seen_concurrent_operations'] = hour_summary['highest_seen_concurrent_operations']
                else:
                    hour_breakdown[timestamp] = hour_summary

            # Compile repo_stats
            ##### Build out based on file_statistics ####################################


            # Compile Operations stats


