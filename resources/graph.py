import matplotlib.pyplot as plt
import numpy as np

class Graph:
    def graph_parsed(node, hourly_breakdown, system_stats, dark_mode, verbose):
        all_chrono_days = Graph.sort_days(hourly_breakdown.keys())

        # Setup base graph details and colors
        if dark_mode is True:
            Graph.set_colors_dark()
        else:
            Graph.set_colors_light()

        # Line Graphs
        Graph.clones(node, all_chrono_days, hourly_breakdown)
        Graph.shallow_clones(node, all_chrono_days, hourly_breakdown)
        Graph.ref_ads(node, all_chrono_days, hourly_breakdown)
        Graph.fetches(node, all_chrono_days, hourly_breakdown)
        Graph.pushes(node, all_chrono_days, hourly_breakdown)
        Graph.ref_ads(node, all_chrono_days, hourly_breakdown)
        Graph.summary(node, all_chrono_days, hourly_breakdown)
        Graph.max_connections(node, all_chrono_days, hourly_breakdown)
        Graph.protocols(node, all_chrono_days, hourly_breakdown)

        # Pie Graphs
        Graph.operations(node, system_stats['operations'])
        plt.close('all')

        # Stacked and Grouped Bar Graphs for repos
        top_clones, top_shallows, top_fetches, top_pushes, top_activity = Graph.sort_top_repos(system_stats['repo_stats'])

        Graph.top_clones(node, top_clones)
        Graph.top_shallows(node, top_shallows)
        Graph.top_fetches(node, top_fetches)
        Graph.top_pushes(node, top_pushes)
        Graph.top_activity(node, top_activity)
        plt.close("all")

        return

    def sort_days(hourly_breakdown_keys):
        # list all days in chronoligical order
        all_chrono_days = list(hourly_breakdown_keys)
        all_chrono_days.sort()
        return all_chrono_days

    def set_colors_light():
        Graph.blue='#001a87'
        Graph.lightblue='#4287f5'
        Graph.green='#067300'
        Graph.lightgreen='#56d658'
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

    def fetches(node, all_chrono_days, hourly_breakdown):
        Graph.set_generic_graph_details()
        fetch_data = []
        date_labels = []
        hours = range(0, 24)
        for day in all_chrono_days:
            for hour in hours:
                date_to_use = f"{str(day)[:4]}-{str(day)[4:6]}-{str(day)[6:8]} {hour:02d}"
                date_labels.append(str(date_to_use))
                try:
                    fetch_data.append(hourly_breakdown[day][hour]['total_fetches'])
                except KeyError:
                    # start of day may not be at 0 so this fills in the blanks to have a complete 24 hour day
                    fetch_data.append(0)

        plt.plot(date_labels, fetch_data, '-', color=Graph.green, label="All Fetches")
        plt.fill_between(date_labels, fetch_data, color=Graph.green, alpha=0.35)
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
#        plt.ylabel('Number of pushes', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-pushes.jpg', dpi=500)
        plt.clf()
        return("Pushes")

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
                    fetch_data.append(hourly_breakdown[day][hour]['total_fetches'])
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
#        plt.ylabel('Number of Git Operations', fontdict={'fontweight': 'bold', 'fontsize': 14})

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
        labels, wedges = Graph.get_operation_decending_order(operations)
        colors = [Graph.blue, Graph.green, Graph.cyan, Graph.yellow, Graph.red]
        plt.pie(wedges, labels=labels, labeldistance=1.12, colors=colors, startangle=90, textprops={'fontweight': 'bold', 'fontsize': 12})
        plt.title(f"Distribution of Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.legend()
        plt.savefig(f'{node}-operations.jpg', dpi=500)
        plt.clf()
        return("Operations")

    def get_operation_decending_order(operations):
        keys = []
        values = []
        for key, value in operations.items():
            if key == "git_http":
                keys.append("Git HTTP")
            elif key == "git_ssh":
                keys.append("Git SSH")
            elif key == "rest":
                keys.append("REST API")
            elif key == "web_ui":
                keys.append("Web UI")
            elif key == "filesystem":
                keys.append("Filesystem")
            values.append(value)
        
        sorted_keys = []
        sorted_values = []
        for x in range(len(operations)):
            index = values.index(max(values))
            sorted_keys.append(keys[index])
            sorted_values.append(values[index])
            del keys[index]
            del values[index]

        return sorted_keys, sorted_values

    def sort_top_repos(repo_stats):
        # Build out first 10 repos (!!! Requires Python3.6+ to ensure dict order !!!)
        first_10_repos = {repo: repo_stats[repo] for repo in list(repo_stats)[:10]}
        top_clones = first_10_repos.copy()
        top_shallows = first_10_repos.copy()
        top_fetches = first_10_repos.copy()
        top_pushes = first_10_repos.copy()
        top_activity = first_10_repos.copy()

        for repo in first_10_repos:
            # Prevent repo from being compared again later
            del repo_stats[repo]

        lowest_clone_repo, lowest_clone_count = Graph.find_lowest_clone(top_clones)
        lowest_shallow_repo, lowest_shallow_count = Graph.find_lowest_shallow(top_shallows)
        lowest_fetch_repo, lowest_fetch_count = Graph.find_lowest_fetch(top_fetches)
        lowest_push_repo, lowest_push_count = Graph.find_lowest_push(top_pushes)
        lowest_activity_repo, lowest_activity_count = Graph.find_lowest_activity(top_activity)

        # For remaining repos, compare stats and replace low activity with higher activity repos respectively
        for repo, stats in repo_stats.items():
            # Clones
            if stats['total_clones'] + stats['total_clone_misses'] > lowest_clone_count:
                del top_clones[lowest_clone_repo]
                top_clones[repo] = stats
                lowest_clone_repo, lowest_clone_count = Graph.find_lowest_clone(top_clones)
            
            # Shallow clones
            if stats['total_shallow_clones'] + stats['total_shallow_clone_misses'] > lowest_shallow_count:
                del top_shallows[lowest_shallow_repo]
                top_shallows[repo] = stats
                lowest_shallow_repo, lowest_shallow_count = Graph.find_lowest_shallow(top_shallows)

            # Fetches
            if stats['total_fetches'] > lowest_fetch_count:
                del top_fetches[lowest_fetch_repo]
                top_fetches[repo] = stats
                lowest_fetch_repo, lowest_fetch_count = Graph.find_lowest_fetch(top_fetches)

            # Pushes
            if stats['total_pushes'] > lowest_push_count:
                del top_pushes[lowest_push_repo]
                top_pushes[repo] = stats
                lowest_push_repo, lowest_push_count = Graph.find_lowest_push(top_pushes)

            # Overall Activity
            if Graph.sum_relevant_stats(stats) > lowest_activity_count:
                del top_activity[lowest_activity_repo]
                top_activity[repo] = stats
                lowest_activity_repo, lowest_activity_count = Graph.find_lowest_activity(top_activity)

        return top_clones, top_shallows, top_fetches, top_pushes, top_activity

    def find_lowest_clone(top_clones):
        values = []
        repos = []
        for repo, stats in top_clones.items():
            values.append(stats['total_clones'] + stats['total_clone_misses'])
            repos.append(repo)
        index = values.index(min(values))

        return repos[index], values[index]

    def find_lowest_shallow(top_shallows):
        values = []
        repos = []
        for repo, stats in top_shallows.items():
            values.append(stats['total_shallow_clones'] + stats['total_shallow_clone_misses'])
            repos.append(repo)
        index = values.index(min(values))

        return repos[index], values[index]

    def find_lowest_fetch(top_fetches):
        values = []
        repos = []
        for repo, stats in top_fetches.items():
            values.append(stats['total_fetches'])
            repos.append(repo)
        index = values.index(min(values))

        return repos[index], values[index]

    def find_lowest_push(top_pushes):
        values = []
        repos = []
        for repo, stats in top_pushes.items():
            values.append(stats['total_pushes'])
            repos.append(repo)
        index = values.index(min(values))

        return repos[index], values[index]

    def find_lowest_activity(top_activity):
        values = []
        repos = []
        for repo, stats in top_activity.items():
            values.append(Graph.sum_relevant_stats(stats))
            repos.append(repo)
        index = values.index(min(values))

        return repos[index], values[index]

    def sum_relevant_stats(stats):
        relevant_sum = stats['total_clones'] + stats['total_clone_misses'] + stats['total_shallow_clones'] + \
                       stats['total_shallow_clone_misses'] + stats['total_fetches'] + stats['total_pushes']
        return relevant_sum

    def top_clones(node, top_clones):
        '''
        Accepts dict{top_clones}
            "top_clones": {
                    repo_identifier: {
                        "total_clones": 0, "total_clone_misses": 2,
                        "total_shallow_clones": 0, "total_shallow_clone_misses": 0,
                        "total_fetches": 0,
                        "total_ref_ads": 174663, "total_ref_ad_miss": 2,
                        "total_pushes": 0
                    }
                    ...
            }
        '''
        Graph.set_generic_graph_details()
        # Build out top ten repos with most interactions (not counting refs)
        labels = []
        clones = []
        clone_misses = []
        shallows = []
        shallow_misses = []
        fetches = []
        pushes = []

        for repo, stats in top_clones.items():
            labels.append(repo.replace('/', ' /\n'))
            clones.append(stats['total_clones'])
            clone_misses.append(stats['total_clone_misses'])
            shallows.append(stats['total_shallow_clones'])
            shallow_misses.append(stats['total_shallow_clone_misses'])
            fetches.append(stats['total_fetches'])
            pushes.append(stats['total_pushes'])

        index = np.arange(len(labels))
        width = 0.2

        p1 = plt.bar(index - width, clones, width, bottom=0, color=Graph.blue)
        p1sub = plt.bar(index - width, clone_misses, width, bottom=clones, color=Graph.lightblue)
        p2 = plt.bar(index, shallows, width, bottom=0, color=Graph.green)
        p2sub = plt.bar(index, shallow_misses, width, bottom=shallows, color=Graph.lightgreen)
        p3 = plt.bar(index + width, fetches, width, color=Graph.red)
        p4 = plt.bar(index + (width * 2), pushes, width, color=Graph.cyan)

        plt.xticks(ticks=(index + width / 2), labels=labels, fontsize=8)
        plt.legend((p1[0], p1sub[0], p2[0], p2sub[0], p3[0], p4[0]), ('Clones', 'Clone Cache Misses', 'Shallow Clones', 'Shallow Clone Cache Misses', 'Fetches', 'Pushes'))
        plt.title(f"Top Ten Cloned Repositories ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.savefig(f'{node}-top_cloned.jpg', dpi=500)
        plt.clf()
        return("Repo Statistics")

    def top_shallows(node, top_shallows):
        pass

    def top_fetches(node, top_fetches):
        pass

    def top_pushes(node, top_pushes):
        pass

    def top_activity(node, top_activity):
        pass
