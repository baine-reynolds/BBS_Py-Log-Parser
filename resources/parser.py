import concurrent.futures
import re

class Parser:
    def start(list_of_access_logs):
        executor = concurrent.futures.ThreadPoolExecutor()
        tasks = []  # storing individual thread details
        all_parsed = []  # all dictionaries that will be compiled later

        for log in list_of_access_logs:
            # start new thread for each log file
            tasks.append(executor.submit(Parser.parse_log, log))
        for thread in concurrent.futures.as_completed(tasks):
            '''
            Each thread.result() will contain a dictionary where there will be 24 keys with each key
            containing a list of result sets. Each key will will be a date/hour timestamp for graphing purposes
            [{"YYYY-MM-DD HH": [logline1_results, logline2_results, ...], "YYYY-MM-DD HH+1": [logline1_results, logline2_results, ...], ...}, ...]
            
            each "result[x]" will contain operation details in the following format:
            
            
            new list object per day
                new dict per hour
                    new list item per log line
            '''
            all_parsed.append(thread.result())
        return compile_results(all_parsed)

    def parse_log(path_to_access_log):
        '''
        open specified log file and parse each line 

        '''
        file_parsed = []
        file_statistics = []
        output_line_indicators = ['o@', 'o*']
        with open(path_to_access_log, 'r') as log:
            for line in log:
                # parse the line and identify key elements
                # find all lines containing "o@" or "o*" to parse
                # retrieve (1: timestamp, 2: protocol (http/ssh) 3, status_code)
                split = line.split(' | ')
                if output_line_indicators in split[3] and len(split) > 12:
                    #ip_address = split[0]   not used
                    protocol = split[1]
                    request_id = split[2]
                    timestamp = split[4]
                    action = split[5]
                    #request_details = split[6]
                    status_code = split[7]
                    git_op = split[10]

                    parsed_timestamp = timestamp.split(':')[0]  # From: "2020-04-27 14:21:23,359" To: "2020-04-27 14"
                    parsed_action = identify_action(protocol, request_id, action, status_code, git_op)
                    if parsed_action == 
                        line_statistic = # key/slug
                        file_statistics.append(line_statistic)


                    line_parsed = {parsed_timestamp:parsed_action}  # {str: list}
                    file_parsed.append(line_parsed)
                elif len(split) < 12:
                    pass # broken line that is commonly found as start/end of a file.
                    # Potentially worth counting for indication of issues but skipping for now.
                elif output_line_indicators not in split[3]:
                    pass # skip input lines as they provide minimal information
                else:
                    print(f"Could not match against the line:\n{split}")
        return file_parsed, file_statistics

    def identify_action(protocol, request_id, action, status_code, git_op):
        """     
        breaks log line to list of booleans (and misc) for operation breakdown. (Boolean unless specified otherwise)
        [clone, clone_miss, shallow, shallow_miss, fetch, fetch_miss, ref_ad, ref_ad_miss,
            push, rest, file_system, web_ui, ssh, http, int(concurrent_connections) ]
        """
        clone, clone_miss = False, False
        shallow, shallow_miss = False, False
        fetch, fetch_miss = False, False
        ref_ad, ref_ad_miss = False, False
        push = False
        rest = False
        file_system = False
        web_ui = False
        ssh = False
        http = False
        concurrent_connections = 0

        concurrent_connections = request_id.split('x')[3]

        actions = action.split(' ')
        if protocol.lower() in ['http', 'https']:
            http = True
            op_type = actions[2].lower  # ignoring get vs post vs delete for now

            if "/rest/api" in op_type:
                # rest api interaction
                rest = True
            elif "/rest/" in op_type:
                # internal REST like permissions
                web_ui = True                
            elif "/scm/" in op_type:
                # git operation
                if int(status_code) in range(200,299):
                    if "push" in git_op:
                        push = True
                    elif "clone" in git_op:
                        if "shallow" in git_op:
                            if "miss" in git_op:
                                shallow_miss = True
                            elif "hit" in git_op:
                                shallow = True
                            else:
                                print(f"Unknown state, passing. Code 10000\n{git_op}")
                                pass
                        else: # non-shallow
                            if "miss" in git_op:
                                clone_miss = True
                            elif "hit" in git_op:
                                clone = True
                            else:
                                print(f"Unknown state, passing. Code 10001\n{git_op}")
                    elif "fetch" in git_op:
                        if "miss" in git_op:
                            fetch_miss = True
                        elif "hit" in git_op:
                            fetch = True
                        elif "bypass" in git_op:
                            # not sure    #############################################################
                            pass
                        else:
                            print(f"Unknown state, passing. Code 10002\n{git_op}")
                    elif "refs" in git_op:
                        if "miss" in git_op:
                            ref_ad_miss = True
                        elif "hit" in git_op:
                            ref_ad = True
                        elif "bypass" in git_op:
                            # not sure    #############################################################
                            pass
                        else:
                            print("Unknown state, passing. Code 10003")
                    else:
                        print(f"Unknown state, passing. Code 10004\n{git_op}")
                        
                else:
                    # parsing out initial auth requests as a single http git op takes 3 requests
                    pass
            elif "/plugins/servlet" in op_type:
                # internal features (includes webhooks, permissions, integrations)
                # not sure    #############################################################
                pass
            elif [x for x in ["/s/", "/download/"] if(x in op_type)]:
                # static file request from WebUI
                # /projects, /users, 
                file_system = True
            
            elif [x for x in ["/admin/", "account", "/dashboard", "/mvc/"] if(x in op_type)]: 
                # any matches for the above list identifying WebUI interactions
                web_ui = True
            else:
                print(f"Cannot parse line, please update Parser.identify_action with appropreiate use case for:\n{op_type}")
        elif protocol.lower() == "ssh":
            if "push" in git_op:
                push = True
            elif  "clone" in git_op:
                if "shallow" in git_op:
                    if "miss" in git_op:
                        shallow_miss = True
                    elif "hit" in git_op:
                        shallow = True
                    elif "bypass" in git_op:
                        # not sure    #############################################################
                        pass
                    else:
                        print(f"unknown state, passing. Code 10005\n{git_op}")
                        pass
                if "miss" in git_op:
                    clone_miss = True
                elif "hit" in git_op:
                    clone = True
                elif "bypass" in git_op:
                    # not sure    #############################################################
                else:
                    print(f"Unknown state, passing. Code 10006\n{git_op}")
                    pass
            elif "fetch" in git_op:
                if "miss" in git_op:
                    fetch_miss = True
                elif "hit" in git_op:
                    fetch = True
                elif "bypass" in git_op:
                    # not sure    #############################################################
                    pass
                else:
                    print(f"Unknown state, passing. Code 10007\n{git_op}")
                    pass
            elif "refs" in git_op:
                if "miss" in git_op:
                    ref_ad_miss = True
                elif "hit" in git_op:
                    ref_ad = True
                elif "bypass" in git_op:
                    # not sure    #############################################################
                else:
                    print(f"Unknown state, passing. Code 10008\n{git_op}")
        else:
            print(f"Could not parse protocol: '{protocol}' properly")

        return [clone, clone_miss, shallow, shallow_miss, fetch, fetch_miss, ref_ad,
                ref_ad_miss, push, rest, file_system, web_ui, ssh, http, concurrent_connections]

    def complie_results(all_days):
        all_parsed_logs = []
        for day_parsed in all_days:  # all_days = list of dictionaries
            date, hour = list(day_parsed.keys())[0].split(' ')
            for hour_parsed in day_parsed:  # day_parsed = dictionary where value = list of lists
                # find total operations per hour
                '''
                Next: ##############################################################################################################################################################################################
                Work on above "for hour_parsed in day_parsed" line above next

                '''
                clone, clone_miss = 0, 0
                shallow, shallow_miss = 0, 0
                fetch, fetch_miss = 0, 0
                ref_ad, ref_ad_miss = 0, 0
                push = 0
                rest = 0
                file_system = 0
                web_ui = 0
                
                ssh = 0
                http = 0
                max_connection = 0

                for item in hour_parsed.values()
                    # Git Operations
                    if item[0] == True:
                        clone += 1
                    elif item[1] == True:
                        clone_miss += 1
                    elif item[2] == True:
                        shallow += 1
                    elif item[3] == True:
                        shallow_miss += 1
                    elif item[4] == True:
                        fetch += 1
                    elif item[5] == True:
                        fetch_miss += 1
                    elif item[6] == True:
                        ref_ad += 1
                    elif item[7] == True:
                        ref_ad_miss += 1
                    elif item[8] == True:
                        push += 1
                    # rest ops
                    elif item[9] == True:
                        rest += 1
                    # file_system ops
                    elif item[10] == True:
                        file_system += 1
                    # web UI ops
                    elif item[11] ==True:
                        web_ui += 1
                    else:
                        print(f"could note identify op type for {item}")
                    
                    if item[12] == "ssh":
                        ssh += 1
                    elif item[12] == "http":
                        http += 1
                    else:
                        # not ssh/http git operation, skipping counter
                        pass
                    
                    if item[13] > max_connection:
                        # find highest peak of the hour for SCM_hosting
                        max_connection = item[13]

                all_parsed_logs.append([date,
                                        hour,
                                        clone,
                                        clone_miss,
                                        shallow,
                                        shallow_miss,
                                        fetch,
                                        fetch_miss,
                                        ref_ad,
                                        ref_ad_miss,
                                        push,
                                        rest,
                                        file_system,
                                        web_ui,
                                        ssh,
                                        http,
                                        max_connection])
            all_days          
        return all_parsed_logs



'''
graph 1:
    total clones (cache hit vs miss)
graph 2:
    total fetches (cache hit vs miss)
graph 3:
    total pushes
graph 4:
    total refs advs (cache hit vs miss)
graph 5:
    total shallow clones (hit vs miss)
graph 6:
    total clone, total fetch, total shallow clone, total push   (ref advs secondary y axis)
graph 7:
    max concurrent operations
graph 8:
    Git http(s) vs ssh operations
graph 9:
    distribute of operations (webUI, git ssh, git http(s) rest, file server)
'''

'''
Data Structures:

Hour breakdown
{"2020-05-06 17":  #date and hour timestamp
    []
}



Total Counts (Summary) 
{"repos": {"key/slug": "number of hits"},
 "filesystem": "number of hits",
 "rest": "number of hits",
 "ssh": "number of hits",
 "http": "number of hits",
 "webui": "number of hits",


    }
'''
