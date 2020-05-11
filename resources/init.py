from optparse import OptionParser
import os, fnmatch

class Init:
    def parse_input():
        parser = OptionParser()
        parser.add_option('-d', '--directory', dest='filepath', help="Path to access logs")
        options, args = parser.parse_args()
        return options, args

    def validate_path(path):
        if path is not None:
            all_files = []
            for root, dirs, files in os.walk(path):
                for name in files:
                    if fnmatch.fnmatch("atlassian-bitbucket-access*", path):
                        all_files.append(os.path.join(root, name))
            if len(all_files) > 0:
                return all_files
            else:
                exit("Could not locate any access logs in given path. Please check the path and try again.")
        else:
            exit("No path specificed, please use the '-d' flag with a path to the access logs.")
