from resources.init import Init
from resources.graph import Graph
from resources.parser import Parser
from os import getcwd
from os import path
from os import remove
import json
import img2pdf

def export_json(node, hourly_breakdown, system_stats):
    write_file = {}
    write_file[node] = [hourly_breakdown, system_stats]
    with open(f'{node}-access_logs_parsed.json', 'w') as out_file:
        json.dump(write_file, out_file)    

def combine_png_to_pdf(node):
    base_dir = getcwd()
    graph_file_names = ["-clones.jpg", "-fetches.jpg", "-pushes.jpg", "-refs.jpg",
                        "-shallow_shallow_clones.jpg", "-summary.jpg", "-operations.jpg"]
    with open(f'{node}.pdf', 'wb') as pdf_output:
        images_to_write = []
        for graph_name in graph_file_names:
            images_to_write.append(path.join(base_dir, node + graph_name))
        pdf_output.write(img2pdf.convert(images_to_write))
        # Clean up the individual image files now that they are compiled into a pdf
        for image in images_to_write:
            remove(image)

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
            #print(f"Created graph .jpg files for '{node}' in working directory")
            combine_png_to_pdf(node)
            print(f"Created pdf of all graphs for {node} found at {node}.pdf")


if __name__ == '__main__':
    main()