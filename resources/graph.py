import matplotlib.pyplot as plt
import concurrent.futures

class Graph:
    def graph_parsed(node, hourly_breakdown, system_stats, dark_mode, verbose):
        tasks = []
        executor = concurrent.futures.ProcessPoolExecutor()
        all_chrono_days = Graph.sort_days(hourly_breakdown.keys())
        # Line Graphs
        tasks.append(executor.submit(Graph.clones, node, all_chrono_days, hourly_breakdown, dark_mode))
        tasks.append(executor.submit(Graph.fetches, node, all_chrono_days, hourly_breakdown, dark_mode))
        tasks.append(executor.submit(Graph.pushes, node, all_chrono_days, hourly_breakdown, dark_mode))
        tasks.append(executor.submit(Graph.ref_ads, node, all_chrono_days, hourly_breakdown, dark_mode))
        tasks.append(executor.submit(Graph.shallow_clones, node, all_chrono_days, hourly_breakdown, dark_mode))
        tasks.append(executor.submit(Graph.summary, node, all_chrono_days, hourly_breakdown, dark_mode))
        tasks.append(executor.submit(Graph.max_connections, node, all_chrono_days, hourly_breakdown, dark_mode))
        tasks.append(executor.submit(Graph.protocols, node, all_chrono_days, hourly_breakdown, dark_mode))

        # Pie Graphs
        tasks.append(executor.submit(Graph.operations, node, system_stats['operations'], dark_mode))
        for task in concurrent.futures.as_completed(tasks):
            if verbose:
                print(f"Graph complete: {task.result()}")

#        Graph.clones(node, all_chrono_days, hourly_breakdown, dark_mode)
#        Graph.fetches(node, all_chrono_days, hourly_breakdown, dark_mode)
#        Graph.pushes(node, all_chrono_days, hourly_breakdown, dark_mode)
#        Graph.ref_ads(node, all_chrono_days, hourly_breakdown, dark_mode)
#        Graph.shallow_clones(node, all_chrono_days, hourly_breakdown, dark_mode)
#        Graph.summary(node, all_chrono_days, hourly_breakdown, dark_mode)
#        Graph.max_connections(node, all_chrono_days, hourly_breakdown, dark_mode)
#        Graph.protocols(node, all_chrono_days, hourly_breakdown, dark_mode)

        #Graph.repos(system_stats['repo_stats'], dark_mode)
#        Graph.operations(node, system_stats['operations'], dark_mode)
        return

    def sort_days(hourly_breakdown_keys):
        # list all days in chronoligical order
        all_chrono_days = list(hourly_breakdown_keys)
        all_chrono_days.sort()
        return all_chrono_days

    def clones(node, all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        plt.plot(date_labels, clone_hit_data, 'g-', label="Clone/Cache Hit")
        plt.plot(date_labels, clone_miss_data, 'r-', label="Clone/Cache Miss")
        plt.fill_between(date_labels, clone_hit_data, color='green', alpha=0.25)
        plt.fill_between(date_labels, clone_miss_data, color='red', alpha=0.25)
        plt.plot(date_labels, clone_all_data, 'b-', label="All Clones")
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title(f"Clone Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of Clones', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-clones.jpg', dpi=500)
        return("Clones")

    def fetches(node, all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        plt.plot(date_labels, fetch_hit_data, 'g-', label="Fetch/Cache Hit")
        plt.plot(date_labels, fetch_miss_data, 'r-', label="Fetch/Cache Miss")
        plt.fill_between(date_labels, fetch_hit_data, color='green', alpha=0.25)
        plt.fill_between(date_labels, fetch_miss_data, color='red', alpha=0.25)
        plt.plot(date_labels, fetch_all_data, 'b-', label="All Fetches")
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title(f"Fetch Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of Fetches', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-fetches.jpg', dpi=500)
        return("Fetches")

    def pushes(node, all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        plt.plot(date_labels, push_all_data, 'c-', label="All pushes")
        plt.fill_between(date_labels, push_all_data, color='cyan', alpha=0.25)
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title(f"push Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of pushes', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-pushes.jpg', dpi=500)
        return("Pushes")

    def ref_ads(node, all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        plt.plot(date_labels, ref_ad_hit_data, 'g-', label="ref/Cache Hit")
        plt.plot(date_labels, ref_ad_miss_data, 'r-', label="ref/Cache Miss")
        plt.fill_between(date_labels, ref_ad_hit_data, color='green', alpha=0.25)
        plt.fill_between(date_labels, ref_ad_miss_data, color='red', alpha=0.25)
        plt.plot(date_labels, ref_ad_all_data, 'b-', label="All refs")
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title(f"ref Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of refs', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-refs.jpg', dpi=500)
        return("Ref Advertisements")

    def shallow_clones(node, all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        plt.plot(date_labels, shallow_clone_hit_data, 'g-', label="shallow_clone/Cache Hit")
        plt.plot(date_labels, shallow_clone_miss_data, 'r-', label="shallow_clone/Cache Miss")
        plt.fill_between(date_labels, shallow_clone_hit_data, color='green', alpha=0.25)
        plt.fill_between(date_labels, shallow_clone_miss_data, color='red', alpha=0.25)
        plt.plot(date_labels, shallow_clone_all_data, 'b-', label="All shallow_clones")
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title(f"shallow_clone Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of shallow_clones', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-shallow_shallow_clones.jpg', dpi=500)
        return("Shallow Clones")

    def summary(node, all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        plt.plot(date_labels, clone_data, 'r-', label="All Clones")
        plt.plot(date_labels, shallow_data, 'y-', label="All Shallow Clones")
        plt.plot(date_labels, fetch_data, 'g-', label="All Fetches")
        plt.plot(date_labels, push_data, 'c-', label="All Pushes")
        plt.fill_between(date_labels, clone_data, color='red', alpha=0.25)
        plt.fill_between(date_labels, shallow_data, color='yellow', alpha=0.25)
        plt.fill_between(date_labels, fetch_data, color='green', alpha=0.25)
        plt.fill_between(date_labels, push_data, color='cyan', alpha=0.25)
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title(f"All Operations Summarized ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        #plt.ylabel('Number of Git Operations', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig(f'{node}-summary.jpg', dpi=500)
        return("Summary")

    def max_connections(node, all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        plt.plot(date_labels, max_connections_data, 'b-', label="Max Concurrent Connections")
        plt.fill_between(date_labels, max_connections_data, color='blue', alpha=0.25)
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title(f"Maximum Concurrent SCM-Hosting Operations ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])

        plt.savefig(f'{node}-max_connections.jpg', dpi=500)
        return("Max Connections")

    def protocols(node, all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(16,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        plt.plot(date_labels, ssh_operations_data, 'r-', label="Git SSH Operations") 
        plt.plot(date_labels, http_operations_data, 'g-', label="Git HTTP Operations")
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title(f"Git Protocols ({node})", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])

        plt.savefig(f'{node}-protocols.jpg', dpi=500)
        return("Git Protocols")

    def repos(repo_stats, dark_mode):
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
        Returns path to saved pie chart
        '''
        pass
        # Per repository
        #for repo_identifier in repo_stats:
            
        #plt.title(f"")
        #labels = [""]

    def operations(node, operations, dark_mode):
        '''
        Accepts dict{operations}
            "operations": {
                           "git_http": int,
                           "git_ssh": int,
                           "rest": int,
                           "web_ui": int,
                           "filesystem": int}
        
        Returns path to saved pie chart file
        '''
        plt.figure(figsize=(16,10))
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'white'}
            plt.style.use('dark_background')
        
        labels = ["git http", "git ssh", "rest", "web_ui", "filesystem"]
        plt.pie([operations['git_http'], operations['git_ssh'], operations['rest'], operations['web_ui'], operations['filesystem']], labels=labels, textprops=textprops)
        plt.title(f"Distribution of Operations ({node})")
        #plt.xlabel('')
        #plt.ylabel('')
        plt.savefig(f'{node}-operations.jpg', dpi=500)
        return("Operations")






'''
graph 1:
    total clones (cache hit vs miss)
graph 2:
    total fetches (cache hit vs miss)
graph 3:
    total pushes
graph 4:
    total refs advs (cache hit vs miss)
graph 5:
    total shallow clones (hit vs miss)
graph 6:
    total clone, total fetch, total shallow clone, total push   (ref advs secondary y axis)
graph 7:
    max concurrent operations
graph 8:
    Git http(s) vs ssh operations


graph 9:
    top 10 repo clones
graph 10:
    top 10 repo fetches
graph 11:
    top 10 repo pushes
graph 12:
    top 10 repo refs
graph 13:
    distribution of operations (webUI, git ssh, git http(s) rest, file server)
'''
