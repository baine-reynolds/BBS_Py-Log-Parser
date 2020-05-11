from resources.init import Init
from resources.parser import Parser
from resources.graph import Graph

def main():
    options, args = Init.parse_input()
    all_access_logs = Init.validate_path(options.filepath)
    parsed_logs = Parser.start(all_access_logs)
    graph_saved_path = Graph.graph_parsed(parsed_logs)
    exit(f"Created pdf at {graph_saved_path}")
