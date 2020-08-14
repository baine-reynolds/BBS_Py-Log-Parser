from optparse import OptionParser
import os, fnmatch

class Init:
    def parse_input():
        '''
        Reads in attributes during run time and sets usage flags appropriately.
        '''
        parser = OptionParser()
        parser.add_option('-p', '--path', dest='filepath', help="Path to access logs")
        parser.add_option('-j', '--json', dest='json', default=False, action="store_true", help='Exports raw data to json rather than graphing')
        parser.add_option('-d', '--dark', dest='dark_mode', default=False, action="store_true", help='Sets Graphs to use dark backdrops')
        parser.add_option('-v', '--verbose', dest='verbose', default=False, action="store_true", help='Sets verbose logging to enabled')
        parser.add_option('-t', '--throttle-graph', dest='throttle_graph', default=None, action="store_const", const=1, help='Throttle Graph creation to a single CPU if encountering issues with graphing library')
        options, args = parser.parse_args()
        return options, args

    def validate_path(provided_path):
        '''
        Accepts the file path given to ensure that atleast 1 file matches the access log naming convention.
        Returns a list of full paths (os.path) to each file located/matched to "atlassian-bitbucket-access*".
        '''
        all_nodes = {}
        if provided_path is not None:
            for root, dirs, files in os.walk(provided_path):
                for name in files:
                    if fnmatch.fnmatch(name, "atlassian-bitbucket-access*"):
                        path_to_log = os.path.join(root, name)
                        node = Init.identify_node(path_to_log, provided_path)
                        if node not in all_nodes.keys():
                            all_nodes[node] = []
                        all_nodes[node].append(path_to_log)
            if len(all_nodes.keys()) > 0:
                # if logs and nodes were identified, continue
                return all_nodes
            else:
                exit("Could not locate any access logs in given path. Please check the path and try again.")
        else:
            exit("No path specificed, please use the '-d' flag with a path to the access logs.")

    def identify_node(path_to_log, provided_path):
        # To ensure consistent pathing expectations, remove a tailing '/' from "provided_path" if present
        if provided_path[-1] == "/":
            provided_path = provided_path[:-1]
        # Reduces path to only the sub-directories after the given parent path
        short_path = path_to_log.replace(provided_path, "")
        list_short_path = short_path.split('/')
        try:
            # If path_provided = ".../SSP-12345" (Multi-node sub-dirs each containing ./node-*/application-logs/atlassian-bitbucket-access*.log)
            if "access" in list_short_path[3]:
                node = list_short_path[1]
        except IndexError:
            try:
                # if path_provided = ".../node-1/" (single node with a ./application-logs/atlassian-bitbucket-access*.log)
                if "access" in list_short_path[2]:
                    # Assume single node is given, supply "Node 1" as the node name
                    node = "Node 1"
            except IndexError:
                try:
                    # If path_provided = ".../application-logs/" (single node containing ./atlassian-bitbucket-access*.log)
                    if "access" in list_short_path[1]:
                        # Assume single node is given, supply "Node 1" as the node name
                        node = "Node 1"
                except IndexError:
                    exit("Access logs not within expected folder structure, please check the path given and try again.")
        return node
