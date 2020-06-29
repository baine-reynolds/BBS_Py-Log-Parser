import matplotlib.pyplot as plt

class Graph:
    def graph_parsed(node, hourly_breakdown, system_stats, dark_mode, verbose):
        all_chrono_days = Graph.sort_days(hourly_breakdown.keys())

        # Setup base graph details and colors
        if dark_mode == True:
            Graph.set_colors_dark()
        else:
            Graph.set_colors_light()

        # Line Graphs
        Graph.clones(node, all_chrono_days, hourly_breakdown)
        Graph.fetches(node, all_chrono_days, hourly_breakdown)
        Graph.pushes(node, all_chrono_days, hourly_breakdown)
        Graph.ref_ads(node, all_chrono_days, hourly_breakdown)
        Graph.shallow_clones(node, all_chrono_days, hourly_breakdown)
        Graph.summary(node, all_chrono_days, hourly_breakdown)
        Graph.max_connections(node, all_chrono_days, hourly_breakdown)
        Graph.protocols(node, all_chrono_days, hourly_breakdown)

        # Pie Graphs
        #Graph.repos(node, system_stats['repo_stats'])
        Graph.operations(node, system_stats['operations'])
        plt.close("all")

        return

    def sort_days(hourly_breakdown_keys):
        # list all days in chronoligical order
        all_chrono_days = list(hourly_breakdown_keys)
        all_chrono_days.sort()
        return all_chrono_days

    def set_colors_light():
        Graph.blue='#001a87'
        Graph.green='#067300'
        Graph.red='#940901'
        Graph.yellow='#a5ab03'
        Graph.cyan='#0295a8'
        Graph.plot_style = 'default'

    def set_colors_dark():
        Graph.blue='#11249c'  
        Graph.green='#11520d'
        Graph.red='#5e130e'
        Graph.yellow='#6f7314'
        Graph.cyan='#167682'
        Graph.plot_style = 'dark_background'

    def set_generic_graph_details():
        plt.style.use(Graph.plot_style)
        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)

    def clones(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        clone_all_data = []
        clone_hit_data = []
        clone_miss_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    clone_all_data.append(hourly_breakdown[day][hour]['total_clones'] + hourly_breakdown[day][hour]['total_clone_misses'])
                    clone_hit_data.append(hourly_breakdown[day][hour]['total_clones'])
                    clone_miss_data.append(hourly_breakdown[day][hour]['total_clone_misses'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    clone_all_data.append(0)
                    clone_hit_data.append(0)
                    clone_miss_data.append(0)

        plt.plot(date_labels, clone_hit_data, '-', color=Graph.green, label="Clone/Cache Hit")
        plt.plot(date_labels, clone_miss_data, '-', color=Graph.red, label="Clone/Cache Miss")
        plt.fill_between(date_labels, clone_hit_data, color=Graph.green, alpha=0.35)
        plt.fill_between(date_labels, clone_miss_data, color=Graph.red, alpha=0.35)
        plt.plot(date_labels, clone_all_data, '-', color=Graph.blue, label="All Clones")
        plt.title(f"Clone Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')        
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of Clones', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-clones.jpg', dpi=500)
        plt.clf()
        return("Clones")

    def fetches(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        fetch_all_data = []
        fetch_hit_data = []
        fetch_miss_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    fetch_all_data.append(hourly_breakdown[day][hour]['total_fetches'] + hourly_breakdown[day][hour]['total_fetch_misses'])
                    fetch_hit_data.append(hourly_breakdown[day][hour]['total_fetches'])
                    fetch_miss_data.append(hourly_breakdown[day][hour]['total_fetch_misses'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    fetch_all_data.append(0)
                    fetch_hit_data.append(0)
                    fetch_miss_data.append(0)

        plt.plot(date_labels, fetch_hit_data, '-', color=Graph.green, label="Fetch/Cache Hit")
        plt.plot(date_labels, fetch_miss_data, '-', color=Graph.red, label="Fetch/Cache Miss")
        plt.fill_between(date_labels, fetch_hit_data, color=Graph.green, alpha=0.35)
        plt.fill_between(date_labels, fetch_miss_data, color=Graph.red, alpha=0.35)
        plt.plot(date_labels, fetch_all_data, '-', color=Graph.blue, label="All Fetches")
        plt.title(f"Fetch Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of Fetches', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-fetches.jpg', dpi=500)
        plt.clf()
        return("Fetches")

    def pushes(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        push_all_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    push_all_data.append(hourly_breakdown[day][hour]['total_pushes'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    push_all_data.append(0)

        plt.plot(date_labels, push_all_data, '-', color=Graph.cyan, label="All Pushes")
        plt.fill_between(date_labels, push_all_data, color=Graph.cyan, alpha=0.35)
        plt.title(f"push Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of pushes', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-pushes.jpg', dpi=500)
        plt.clf()
        return("Pushes")

    def ref_ads(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        ref_ad_all_data = []
        ref_ad_hit_data = []
        ref_ad_miss_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    ref_ad_all_data.append(hourly_breakdown[day][hour]['total_ref_ads'] + hourly_breakdown[day][hour]['total_ref_ad_misses'])
                    ref_ad_hit_data.append(hourly_breakdown[day][hour]['total_ref_ads'])
                    ref_ad_miss_data.append(hourly_breakdown[day][hour]['total_ref_ad_misses'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    ref_ad_all_data.append(0)
                    ref_ad_hit_data.append(0)
                    ref_ad_miss_data.append(0)

        plt.plot(date_labels, ref_ad_hit_data, '-', color=Graph.green, label="Ref Advertisement/Cache Hit")
        plt.plot(date_labels, ref_ad_miss_data, '-', color=Graph.red, label="Ref Advertisement/Cache Miss")
        plt.fill_between(date_labels, ref_ad_hit_data, color=Graph.green, alpha=0.35)
        plt.fill_between(date_labels, ref_ad_miss_data, color=Graph.red, alpha=0.35)
        plt.plot(date_labels, ref_ad_all_data, '-', color=Graph.blue, label="All refs")
        plt.title(f"ref Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of refs', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-refs.jpg', dpi=500)
        plt.clf()
        return("Ref Advertisements")

    def shallow_clones(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        shallow_clone_all_data = []
        shallow_clone_hit_data = []
        shallow_clone_miss_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    shallow_clone_all_data.append(hourly_breakdown[day][hour]['total_shallow_clones'] + hourly_breakdown[day][hour]['total_shallow_clone_misses'])
                    shallow_clone_hit_data.append(hourly_breakdown[day][hour]['total_shallow_clones'])
                    shallow_clone_miss_data.append(hourly_breakdown[day][hour]['total_shallow_clone_misses'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    shallow_clone_all_data.append(0)
                    shallow_clone_hit_data.append(0)
                    shallow_clone_miss_data.append(0)

        plt.plot(date_labels, shallow_clone_hit_data, '-', color=Graph.green, label="Shallow Clone/Cache Hit")
        plt.plot(date_labels, shallow_clone_miss_data, '-', color=Graph.red, label="Shallow Clone/Cache Miss")
        plt.fill_between(date_labels, shallow_clone_hit_data, color=Graph.green, alpha=0.35)
        plt.fill_between(date_labels, shallow_clone_miss_data, color=Graph.red, alpha=0.35)
        plt.plot(date_labels, shallow_clone_all_data, '-', color=Graph.blue, label="All Shallow Clones")
        plt.title(f"Shallow Clone Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of shallow_clones', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-shallow_shallow_clones.jpg', dpi=500)
        plt.clf()
        return("Shallow Clones")

    def summary(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        clone_data = []
        shallow_data = []
        fetch_data = []
        push_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    clone_data.append(hourly_breakdown[day][hour]['total_clones'] + hourly_breakdown[day][hour]['total_clone_misses'])
                    shallow_data.append(hourly_breakdown[day][hour]['total_shallow_clones'] + hourly_breakdown[day][hour]['total_shallow_clone_misses'])
                    fetch_data.append(hourly_breakdown[day][hour]['total_fetches'] + hourly_breakdown[day][hour]['total_fetch_misses'])
                    push_data.append(hourly_breakdown[day][hour]['total_pushes'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    clone_data.append(0)
                    shallow_data.append(0)
                    fetch_data.append(0)
                    push_data.append(0)

        plt.plot(date_labels, fetch_data, '-', color=Graph.green, label="All Fetches")
        plt.plot(date_labels, clone_data, '-', color=Graph.red, label="All Clones")
        plt.plot(date_labels, shallow_data, '-', color=Graph.yellow, label="All Shallow Clones")
        plt.plot(date_labels, push_data, '-', color=Graph.cyan, label="All Pushes")
        plt.fill_between(date_labels, fetch_data, color=Graph.green, alpha=0.35)
        plt.fill_between(date_labels, clone_data, color=Graph.red, alpha=0.35)
        plt.fill_between(date_labels, shallow_data, color=Graph.yellow, alpha=0.35)
        plt.fill_between(date_labels, push_data, color=Graph.cyan, alpha=0.35)
        plt.title(f"All Operations Summarized ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of Git Operations', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-summary.jpg', dpi=500)
        plt.clf()
        return("Summary")

    def max_connections(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        max_connections_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    max_connections_data.append(hourly_breakdown[day][hour]['highest_seen_concurrent_operations'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    max_connections_data.append(0)

        plt.plot(date_labels, max_connections_data, '-', color=Graph.blue, label="Max Concurrent Connections")
        plt.fill_between(date_labels, max_connections_data, color=Graph.blue, alpha=0.35)
        plt.title(f"Maximum Concurrent SCM-Hosting Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])

        plt.savefig(f'{node}-max_connections.jpg', dpi=500)
        plt.clf()
        return("Max Connections")

    def protocols(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        ssh_operations_data = []
        http_operations_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    ssh_operations_data.append(hourly_breakdown[day][hour]['total_git_ssh_operations'])
                    http_operations_data.append(hourly_breakdown[day][hour]['total_git_http_operations'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    ssh_operations_data.append(0)
                    http_operations_data.append(0)

        plt.plot(date_labels, ssh_operations_data, '-', color=Graph.red, label="Git SSH Operations") 
        plt.plot(date_labels, http_operations_data, '-', color=Graph.green, label="Git HTTP Operations")
        plt.title(f"Git Protocols ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])

        plt.savefig(f'{node}-protocols.jpg', dpi=500)
        plt.clf()
        return("Git Protocols")

    def repos(node, repo_stats):
        '''
        Accepts dict{repo_stats}
            "repo_stats": {
                    repo_identifier: {
                        "total_clones": 0, "total_clone_misses": 2,
                        "total_shallow_clones": 0, "total_shallow_clone_misses": 0,
                        "total_fetches": 0, "total_fetch_misses": 0,
                        "total_ref_ads": 174663, "total_ref_ad_miss": 2,
                        "total_pushes": 0
                    }
                    ...
            }
        '''
        Graph.set_generic_graph_details()
        top_ten_repos = {}
        # Build out top ten repos with most interactions (not counting refs)
        for repo_identifier in repo_stats:
            total_ops = repo_identifier['total_clones'] + repo_identifier['total_clone_misses'] + \
                        repo_identifier['total_shallow_clones'] + repo_identifier['total_shallow_clone_misses'] + \
                        repo_identifier['total_fatches'] + repo_identifier['total_fetch_misses'] + \
                        repo_identifier['pushes']
            if len(top_ten_repos) < 10:
                top_ten_repos[repo_identifier] = total_ops
            else:
                min_value = min(top_ten_repos.values())
                matching_key = [key for key in top_ten_repos if top_ten_repos[key] == min_value]
                if total_ops > min_value:
                    del top_ten_repos[matching_key]
                    top_ten_repos[repo_identifier] = total_ops

        # Below probably won't work yet, Needs each value passed in    ###############################
        plt.pie(top_ten_repos)
        plt.title(f"Top Ten CLoned Repositories ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.savefig(f'{node}-top_repos.jpg', dpi=500)
        plt.clf()
        return("Repo Statistics")

    def operations(node, operations):
        '''
        Accepts dict{operations}
            "operations": {
                           "git_http": int,
                           "git_ssh": int,
                           "rest": int,
                           "web_ui": int,
                           "filesystem": int}
        '''
        Graph.set_generic_graph_details()
        labels = ["git http", "git ssh", "rest", "web_ui", "filesystem"]
        plt.pie([operations['git_http'], operations['git_ssh'], operations['rest'], operations['web_ui'], operations['filesystem']], labels=labels)
        plt.title(f"Distribution of Operations ({node})")
        #plt.xlabel('')
        #plt.ylabel('')
        plt.savefig(f'{node}-operations.jpg', dpi=500)
        plt.clf()
        return("Operations")
