class IdentifyAction():
    def parse(protocol, request_id, action, status_code, labels, verbose):
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
            if [x for x in ["/scm/"] if (x in op_type)]: # Parse Git operation
                git_type = "http"
                try:
                    if int(status_code) in range(200,299):
                        op_action = IdentifyAction.git_op_action(action, labels)
                    else:
                        op_action = "ignore" # drop 401s and redirects
                except ValueError:
                    # If status_code == "-" then it cannot be converted to an int()
                    pass
            else: # Parse if rest, web_ui, or filesystem
                op_action = IdentifyAction.http_webserver(op_type, verbose)
        elif "ssh" in str(protocol).lower():
            git_type = "ssh"
            op_action = IdentifyAction.git_op_action(action, labels)
        else:
            op_action = "ignore"

        if op_action == "":
            if verbose:
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
            return("push")
        elif "refs" in labels:
            git_action = "refs"
        elif "shallow" in labels: #shallow must be before 'clone' otherwise all shallows will get pooled in with clones
            if "fetch" in labels:
                return("fetch")
            else:
                git_action = "shallow"
        elif "clone" in labels:
            git_action = "clone"
        elif "fetch" in labels:
            return("fetch")
        elif "archive" in labels:
            git_action = "ignore"
        elif "info/refs" in action:
            git_action = "refs"
        elif "git-upload-pack" in action:
            return("unclassified")

        cache = ""  # Cache hit by default
        if git_action == "" or git_action == "ignore":
            pass
        elif "hit" not in labels:  # Cache miss (Accounts for either a "bypass" or "miss")
            cache = "_miss"

        git_op = f"{git_action}{cache}"
        return git_op

    def http_webserver(op_type, verbose):
        ignore_list = ["/favicon.ico", "/avatar.png", "/system/maintenance", "/unavailable",
                       "/j_atl_security_check", "/j_atl_security_logout", "/system/startup",
                       "/getting-started", "/robots.txt"]
        rest_actions = ["/rest/api", "/rest/capabilities", "/status", "/api/v3/rate_limit"]
        filesystem_actions = ["/s/", "/download/"]
        webui_actions = ["/rest", "/admin", "/account", "/dashboard", "/mvc", "/projects", "/captcha",
                         "/repos", "/users", "/login", "/logout", "profile", "/plugins/servlet", "/passwordreset",
                         "/index", "/setup", "/about"]

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
            if verbose:
                print(f"Unable to catagorize the following into [rest, filesystem, web_ui]: '{op_type}'")
            op_action = "ignore"

        return op_action
