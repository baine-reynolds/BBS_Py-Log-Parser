import concurrent.futures
import re

class Parser:
    def start(list_of_access_logs):
        '''
        Accepts list[list_of_access_logs] where each item is a full path to an access log.
        Returns dict{all_parsed_logs} and dict{system_stats}

            dict{all_parsed_logs}
            { YYYYMMDD: {
                        HH: { 
                              "total_clones" = int(counter, default = 0),
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
                        HH: {
                              "total_clones" = int(counter, default = 0),
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
            { YYYYMMDD:
                        {HH: { 
                              "total_clones" = int(counter, default = 0),
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
            ...
            }
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
                             "filesystem": call_counter
            }
        '''
        executor = concurrent.futures.ProcessPoolExecutor()
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
                { YYYYMMDDHH: {
                               HH: {
                                    "total_clones" = int(counter, default = 0),
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
                                "filesystem": call_counter
                                ### potentially add "lfs" here
                              }
                }
        '''
        file_parsed = {}
        default_repo = {"clone": 0, "clone_miss": 0, "shallow": 0, "shallow_miss": 0,
                        "fetch": 0, "fetch_miss": 0, "refs": 0, "refs_miss": 0, "push": 0 }
        file_statistics = {"repo_stats": {}, "operations": {"git_http": 0, "git_ssh": 0, "rest": 0, "web_ui": 0, "filesystem": 0}}
        #output_line_indicators = ['o@', 'o*']
        with open(path_to_access_log, 'r') as log:
            for line in log:
                split = line.split(' | ')
                try:
                    if ("o@" in split[2] and len(split) > 12) or ("o*" in split[2] and len(split) > 12):
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
                        labels = split[10]

                        #parsed_timestamp = timestamp.split(':')[0]  # From: "2020-04-27 14:21:23,359" To: "2020-04-27 14"
                        day, hour = Parser.parse_timestamp(timestamp)

                        parsed_action = Parser.identify_action(protocol, request_id, action, status_code, labels)

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
                            pass # Not a git operation

                        if repo_identifier == None:
                            pass
                        else:
                            # if repo doesn't yet exist, initialize it
                            if parsed_action['op_action'] != "":
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

    def identify_action(protocol, request_id, action, status_code, labels):
        """
        Accepts the following access log fields:
            str(protocol),
            str(request_id),
            str(action),
            str(status_code),
            str(labels)

        Returns a dict{identified_action} containing 2 key/value pairs:
            dict{identified_action}
            {"op_action": str(value),

                "value" must be one of the following strings:
                "clone", "clone_miss", "shallow", "shallow_miss",
                "fetch", "fetch_miss", "refs", "refs_miss",
                "push", "rest", "web_ui", "filesystem",
                "" (default)
                default is only seen if the parsing failed to identify the action
            "max_connections": int(value)
            }
        """
        #print(f"Prototol: {protocol}\nRequest_id: {request_id}\nAction: {action}\nStatus Code: {status_code}\nGit Operation: {labels}")
        op_action = ""
        git_type = ""

        concurrent_connections = int(request_id.split('x')[3])

        actions = action.split(' ')
        if "http" in str(protocol).lower() and (str(status_code) != "404"): # in some cases, status_code can be "-" so converting to string prevents errors
            op_type = actions[1].lower()  # ignoring get vs post vs delete for now
            if [x for x in ["/favicon.ico", "/avatar.png", "/system/maintenance", "/unavailable", "/j_atl_security_check", "/j_atl_security_logout", 
                            "/system/startup", "/getting-started", "/robots.txt"] if(x in op_type)]: 
                # Throw out non-wanted data
                pass
            #elif "/scm/" in op_type:
            elif [x for x in ["/scm/", "/git/"] if (x in op_type)]:
                if status_code == "-" or labels == "-":
                    pass
                elif int(status_code) in range(200,299):  # http 200 range status code
                    # git operation
                    git_type = "http"
                    if "push" in labels:
                        op_action = "push"
                    elif "clone" in labels:
                        if "shallow" in labels:
                            if "miss" in labels:
                                op_action = "shallow_miss"
                            elif "hit" in labels:
                                op_action = "shallow"
                            elif "bypass" in labels:
                                # not sure   #############################################################
                                pass
                            elif "cache" not in labels:
                                op_action = "clone_miss"
                            else:
                                print(f"Unknown state, skipping. Code 10000\n{protocol} | {action} | {labels}")
                                op_action = "invalid"
                        else: # non-shallow
                            if "miss" in labels:
                                op_action = "clone_miss"
                            elif "hit" in labels:
                                op_action = "clone"
                            elif "bypass" in labels:
                                # not sure   #############################################################
                                pass
                            elif "cache" not in labels:
                                op_action = "clone_miss"
                            else:
                                print(f"Unknown state, skipping. Code 10001\n{protocol} | {action} | {labels}")
                    elif "fetch" in labels:
                        if "miss" in labels:
                            op_action = "fetch_miss"
                        elif "hit" in labels:
                            op_action = "fetch"
                        elif "bypass" in labels:
                            # not sure   #############################################################
                            pass
                        elif "cache" not in labels:
                            op_action = "fetch_miss"
                        else:
                            print(f"Unknown state, skipping. Code 10002\n{protocol} | {action} | {labels}")
                    elif "refs" in labels:
                        if "miss" in labels:
                            op_action = "refs_miss"
                        elif "hit" in labels:
                            op_action = "refs"
                        elif "bypass" in labels:
                            # not sure   #############################################################
                            pass
                        elif "cache" not in labels:
                            op_action = "refs_miss"
                        else:
                            print(f"Unknown state, skipping. Code 10003\n{protocol} | {action} | {labels}")
                            pass
                    elif "git-upload-pack" in op_type:
                        # No label is seen but the "git-upload-pack" is present, considering it a clone
                        if "hit" in labels:
                            op_action = "clone"
                        else: # cache miss or no mention
                            op_action = "clone_miss"
                    elif "info/refs" in op_type:
                        if "hit" in labels:
                            op_action = "refs"
                        else: # cache miss or no mention
                            op_action = "refs_miss"
                    elif [x for x in ["capabilities", "negotiation"] if (x in labels)]:
                        # throwing out un-wanted data
                        git_type = "" # clearing git_type as we don't want to count unused data points
                    else:
                        print(f"Unknown state, skipping. Code 10004\n{protocol} | {action} | {labels}")
                        git_type = "" # clearing git_type as we don't want to count unused data points
                        pass
            elif "/plugins/servlet" in op_type:
                # internal features (includes webhooks, permissions, integrations)
                # not sure   #############################################################
                pass
            elif [x for x in ["/rest/api", "/rest/capabilities", "/status", "/api/v3/rate_limit"] if (x in op_type)]:
                # rest api interaction
                op_action = "rest"
            elif [x for x in ["/s/", "/download/"] if(x in op_type)]:
                # static file request from WebUI
                # /projects, /users, 
                op_action = "filesystem"
            elif [x for x in ["/rest", "/admin", "/account", "/dashboard", "/mvc", "/projects", "/repos", "/users", "/login", "/logout", "profile"] if(x in op_type)]: 
                op_action = "web_ui"
                # "/rest/" internal REST like permissions
            elif op_type == "/":  # Exact match root of webserver
                op_action = "web_ui" 
            else:
                print(f"Cannot parse line, please update Parser.identify_action() with appropreiate use case for:\n{protocol} | {action} | {labels} | {status_code}")
                pass
        elif "ssh" in str(protocol).lower():
            git_type = "ssh"
            if "push" in labels:
                op_action = "push"
            elif  "clone" in labels:
                if "shallow" in labels:
                    if "miss" in labels:
                        op_action = "shallow_miss"
                    elif "hit" in labels:
                        op_action = "shallow"
                    elif "bypass" in labels:
                        # not sure   #############################################################
                        pass
                    elif "cache" not in labels:
                        op_action = "shallow_miss"
                    else:
                        print(f"unknown state, skipping. Code 10005\n{protocol} | {action} | {labels}")
                        pass
                if "miss" in labels:
                    op_action = "clone_miss"
                elif "hit" in labels:
                    op_action = "clone"
                elif "bypass" in labels:
                    # not sure   #############################################################
                    pass
                elif "cache" not in labels:
                    op_action = "clone_miss"
                else:
                    print(f"Unknown state, skipping. Code 10006\n{protocol} | {action} | {labels}")
                    pass
            elif "fetch" in labels:
                if "miss" in labels:
                    op_action = "fetch_miss"
                elif "hit" in labels:
                    op_action = "fetch"
                elif "bypass" in labels:
                    # not sure   #############################################################
                    pass
                elif "cache" not in labels:
                    op_action = "fetch_miss"
                else:
                    print(f"Unknown state, skipping. Code 10007\n{protocol} | {action} | {labels}")
                    pass
            elif "refs" in labels:
                if "miss" in labels:
                    op_action = "refs_miss"
                elif "hit" in labels:
                    op_action = "refs"
                elif "bypass" in labels:
                    # not sure   #############################################################
                    op_action = "refs"
                elif "cache" not in labels:
                    op_action = "refs_miss"
                else:
                    print(f"Unknown state, skipping. Code 10008\n{protocol} | {action} | {labels}")
        else:
            # Dropping all http 404 requests to make sure that incorrect endpoints aren't counted
            pass
        identified_action = {"op_action": op_action, "git_type": git_type, "max_connections": concurrent_connections}
        return identified_action

    def merge_hours(file_parsed):
        '''
        Accepts dict{file_parsed}
            file_parsed is a dict who's keys are a int(day) and values are a dict{} who's keys are int(hour) containing a list of dict{parsed_action} from identify_action()
                {YYYYMMDD: {HH: [parsed_action1,
                                 parsed_action2,
                                 ...
                                ],
                            HH: [parsed_action1,
                                 parsed_action2,
                                 ...
                                ],
                            HH: [parsed_action1,
                                 parsed_action2,
                                 ...
                                ],
                            ...
                            }
                }
        Returns dict{parsed_log}
            {YYYYMMDD: {HH: {"total_clones" = int(counter, default = 0),
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
                    elif action['op_action'] == "fetch_miss": file_summarized[day][hour]['total_fetch_misses'] += 1
                    elif action['op_action'] == "refs": file_summarized[day][hour]['total_ref_ads'] += 1
                    elif action['op_action'] == "refs_miss": file_summarized[day][hour]['total_ref_ad_miss'] += 1
                    elif action['op_action'] == "push": file_summarized[day][hour]['total_pushes'] += 1
                    elif action['op_action'] == "rest": file_summarized[day][hour]['total_rest_calls'] += 1
                    elif action['op_action'] == "filesystem": file_summarized[day][hour]['total_filesystem_calls'] += 1
                    elif action['op_action'] == "web_ui": file_summarized[day][hour]['total_webui_calls'] += 1

                    if action['git_type'] == "ssh": file_summarized[day][hour]['total_git_ssh_operations'] += 1
                    elif action['git_type'] == "http": file_summarized[day][hour]['total_git_http_operations'] += 1

                    if action['max_connections'] > file_summarized[day][hour]['highest_seen_concurrent_operations']:
                        file_summarized[day][hour]['highest_seen_concurrent_operations'] = action['max_connections']
        return(file_summarized)

    def compile_results(all_logs):
        '''
        Accepts list[all_logs] where each item is a list containing [file_parsed, file_statistics] from parse_log()

        '''
        all_days = {}
        all_repo_stats = {}
        default_hour = { "total_clones": 0,
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
        default_repo = { "total_clones": 0,
                         "total_clone_misses": 0,
                         "total_shallow_clones": 0,
                         "total_shallow_clone_misses": 0,
                         "total_fetches": 0,
                         "total_fetch_misses": 0,
                         "total_ref_ads": 0,
                         "total_ref_ad_miss": 0,
                         "total_pushes" : 0
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
                    all_days[day][hour]['total_fetch_misses'] += single_file_summarized[day][hour]['total_fetch_misses']
                    all_days[day][hour]['total_ref_ads'] += single_file_summarized[day][hour]['total_ref_ads']
                    all_days[day][hour]['total_ref_ad_miss'] += single_file_summarized[day][hour]['total_ref_ad_miss']
                    all_days[day][hour]['total_pushes'] += single_file_summarized[day][hour]['total_pushes']
                    all_days[day][hour]['total_rest_calls'] += single_file_summarized[day][hour]['total_rest_calls']
                    all_days[day][hour]['total_filesystem_calls'] += single_file_summarized[day][hour]['total_filesystem_calls']
                    all_days[day][hour]['total_webui_calls'] += single_file_summarized[day][hour]['total_webui_calls']
                    all_days[day][hour]['total_git_ssh_operations'] += single_file_summarized[day][hour]['total_git_ssh_operations']
                    all_days[day][hour]['total_git_http_operations'] += single_file_summarized[day][hour]['total_git_http_operations']
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
                all_repo_stats[repo_identifier]['total_fetch_misses'] += single_file_statistics['repo_stats'][repo_identifier]['fetch_miss']
                all_repo_stats[repo_identifier]['total_ref_ads'] += single_file_statistics['repo_stats'][repo_identifier]['refs']
                all_repo_stats[repo_identifier]['total_ref_ad_miss'] += single_file_statistics['repo_stats'][repo_identifier]['refs_miss']
                all_repo_stats[repo_identifier]['total_pushes'] += single_file_statistics['repo_stats'][repo_identifier]['push']

            # Compile Operations stats
            operations['git_http'] += single_file_statistics['operations']['git_http']
            operations['git_ssh'] += single_file_statistics['operations']['git_ssh']
            operations['rest'] += single_file_statistics['operations']['rest']
            operations['web_ui'] += single_file_statistics['operations']['web_ui']
            operations['filesystem'] += single_file_statistics['operations']['filesystem']

        log_stats = {'repo_stats': all_repo_stats, 'operations': operations}
        return all_days, log_stats