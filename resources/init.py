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
        options, args = parser.parse_args()
        return options, args

    def validate_path(path):
        '''
        Accepts the file path given to ensure that atleast 1 file matches the access log naming convention.
        Returns a list of full paths (os.path) to each file located/matched to "atlassian-bitbucket-access*".
        '''
        if path is not None:
            all_files = []
            for root, dirs, files in os.walk(path):
                for name in files:
                    if fnmatch.fnmatch(name, "atlassian-bitbucket-access*"):
                        all_files.append(os.path.join(root, name))
            if len(all_files) > 0:
                return all_files
            else:
                exit("Could not locate any access logs in given path. Please check the path and try again.")
        else:
            exit("No path specificed, please use the '-d' flag with a path to the access logs.")
