
class IdentifyAction():
    def parse_new(protocol, request_id, action, status_code, labels):
        '''
        Accepts: str(protocol), str(request_id), str(action), str(status_code), str(labels)
        Returns: dict{
                      "op_action": str(op_action),
                      "git_type": str(git_type),
                      "max_connections: int(concurrent_connections) 
                     }
        '''
        op_action = ""
        git_type = ""
        concurrent_connections = 0

        if "http" in str(protocol).lower() and (str(status_code) != "404"):
            op_type = action.split(' ')[1].lower()  # ignoring get vs post vs delete for now
            if [x for x in ["/scm/", "/git/"] if (x in op_type)]: # Parse Git operation
                git_type = "http"
                try:
                    if int(status_code) in range(200,299):
                        op_action = IdentifyAction.git_op_action(action, labels)
                except ValueError:
                    # If status_code == "-" then it cannot be converted to an int()
                    pass
            else: # Parse if rest, web_ui, or filesystem
                op_action = IdentifyAction.http_webserver(op_type)
        elif "ssh" in str(protocol).lower():
            git_type = "ssh"
            op_action = IdentifyAction.git_op_action(action, labels)
        else:
            op_action = "ignore"

        if op_action == "":
            print(f"Cannot parse line, please update IdentifyAction.parse() with appropreiate use case for:\n{protocol} | {action} | {labels} | {status_code}")
        elif op_action == "ignore":
            pass
        # Break request_id and find concurrent SCM-hosting ticket count
        concurrent_connections = int(request_id.split('x')[3])

        identified_action = {"op_action": op_action, "git_type": git_type, "max_connections": concurrent_connections}
        return identified_action

    def git_op_action(action, labels):
        git_action = ""
        if "push" in labels or "git-receive-pack" in action:
            #git_action = "push"
            return("push")
        elif "refs" in labels or "info/refs" in action:
            git_action = "refs"
        elif "shallow" in labels:
            git_action = "shallow"
        elif "clone" in labels:
            git_action = "clone"
        elif "fetch" in labels or "git-upload-pack" in action:
            git_action = "fetch"

        cache = ""  # Cache hit by default
        if git_action == "":
            pass
        #elif "cache" not in labels:  # Server's too busy to add labels
        #    cache = "_miss" # potentionally switch to "_busy"
        elif "hit" not in labels:  # Cache miss (Accounts for either a "bypass" or "miss")
            cache = "_miss"

        git_op = f"{git_action}{cache}"
        return git_op

    def http_webserver(op_type):
        ignore_list = ["/favicon.ico", "/avatar.png", "/system/maintenance", "/unavailable",
                      "/j_atl_security_check", "/j_atl_security_logout", "/system/startup",
                      "/getting-started", "/robots.txt"]
        rest_actions = ["/rest/api", "/rest/capabilities", "/status", "/api/v3/rate_limit"]
        filesystem_actions = ["/s/", "/download/"]
        webui_actions = ["/rest", "/admin", "/account", "/dashboard", "/mvc", "/projects",
                         "/repos", "/users", "/login", "/logout", "profile", "/plugins/servlet"]

        op_action = ""

        if [x for x in ignore_list if(x in op_type)]:
            op_action = "ignore"
        elif [x for x in rest_actions if(x in op_type)]:
            op_action = "rest"
        elif [x for x in filesystem_actions if(x in op_type)]:
            op_action = "filesystem"
        elif [x for x in webui_actions if(x in op_type)]:
            op_action = "web_ui" 
        elif op_type == "/":  # Exact match root of webserver
            op_action = "web_ui"
        else:
            print(f"Unable to catagorize the following into [rest, filesystem, web_ui]: '{op_type}'")
            op_action = "ignore"

        return op_action

    def parse_old(protocol, request_id, action, status_code, labels):
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