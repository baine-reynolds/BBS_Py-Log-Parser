class Parser:
    def start(list_of_access_logs, verbose):
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
                              "total_ref_ad_misses" = int(counter, default = 0),
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
                              "total_ref_ad_misses" = int(counter, default = 0),
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
                              "total_ref_ad_misses" = int(counter, default = 0),
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
                                                "total_ref_ad_misses" = int(counter, default = 0),
                                                "total_pushes" = int(counter, default = 0)
                                               },
                             repo_identifier: { "total_clones" = int(counter, default = 0),
                                                "total_clone_misses" = int(counter, default = 0),
                                                "total_shallow_clones" = int(counter, default = 0),
                                                "total_shallow_clone_misses" = int(counter, default = 0),
                                                "total_fetches" = int(counter, default = 0),
                                                "total_fetch_misses" = int(counter, default = 0),
                                                "total_ref_ads" = int(counter, default = 0),
                                                "total_ref_ad_misses" = int(counter, default = 0),
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

    def parse_log(path_to_access_log, verbose):
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
                                    "total_ref_ad_misses" = int(counter, default = 0),
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
                                                     "total_ref_ad_misses" = int(counter, default = 0),
                                                     "total_pushes" = int(counter, default = 0)
                                                  },
                                repo_identifier: { "total_clones" = int(counter, default = 0),
                                                   "total_clone_misses" = int(counter, default = 0),
                                                   "total_shallow_clones" = int(counter, default = 0),
                                                   "total_shallow_clone_misses" = int(counter, default = 0),
                                                   "total_fetches" = int(counter, default = 0),
                                                   "total_fetch_misses" = int(counter, default = 0),
                                                   "total_ref_ads" = int(counter, default = 0),
                                                   "total_ref_ad_misses" = int(counter, default = 0),
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
    def merge_hours(file_parsed):
        '''
        Accepts dict{file_parsed}
            file_parsed is a dict who's keys are a int(day) and values are a dict{} who's keys are int(hour) containing a list of dict{parsed_action} from IdentifyAction.parse()
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
                             "total_ref_ad_misses" = int(counter, default = 0),
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





