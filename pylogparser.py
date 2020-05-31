from resources.init import Init
from resources.graph import Graph
from resources.parser import Parser
import json


def export_json(all_access_logs):
    with open('access_logs_parsed.json', 'w') as out_file:
        json.dump(all_access_logs, out_file)
    

def main():
    options, args = Init.parse_input()
    all_access_logs = Init.validate_path(options.filepath)
    parsed_logs = Parser.start(all_access_logs)
    if options.json == True:
        export_json(all_access_logs)
        exit("Created 'access_logs_parsed.json' in working directory")
    else:
        Graph.graph_parsed(parsed_logs)
        exit("Created pdfs in working directory")


if __name__ == '__main__':
    main()