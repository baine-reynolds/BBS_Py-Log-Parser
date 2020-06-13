from resources.init import Init
from resources.graph import Graph
from resources.parser import Parser
import json


def export_json(node, hourly_breakdown, system_stats):
    write_file = {}
    write_file[node] = [hourly_breakdown, system_stats]
    with open(f'{node}-access_logs_parsed.json', 'w') as out_file:
        json.dump(write_file, out_file)    


def main():
    options, args = Init.parse_input()
    all_nodes = Init.validate_path(options.filepath)
    for node in all_nodes:
        hourly_breakdown, system_stats = Parser.start(all_nodes[node])
        if options.json == True:
            export_json(node, hourly_breakdown, system_stats)
            print(f"Created '{node}-access_logs_parsed.json' in working directory")
        else:
            Graph.graph_parsed(node, hourly_breakdown, system_stats, options.dark_mode)
            print(f"Created graph .png files for '{node}' in working directory")


if __name__ == '__main__':
    main()