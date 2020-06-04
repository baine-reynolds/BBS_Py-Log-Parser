from resources.init import Init
from resources.graph import Graph
from resources.parser import Parser
import json


def export_json(hourly_breakdown, system_stats):
    with open('access_logs_parsed.json', 'w') as out_file:
        json.dump(hourly_breakdown, out_file)
        json.dump(system_stats, out_file)
    

def main():
    options, args = Init.parse_input()
    all_access_logs = Init.validate_path(options.filepath)
    hourly_breakdown, system_stats = Parser.start(all_access_logs)
    if options.json == True:
        export_json(hourly_breakdown, system_stats)
        exit("Created 'access_logs_parsed.json' in working directory")
    else:
        Graph.graph_parsed(hourly_breakdown, system_stats)
        exit("Created pdfs in working directory")


if __name__ == '__main__':
    main()