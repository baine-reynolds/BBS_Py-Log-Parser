import matplotlib.pyplot as plt

class Graph:
    def graph_parsed(hourly_breakdown, system_stats, dark_mode):
        all_chrono_days = Graph.sort_days(hourly_breakdown.keys())
        Graph.clones(all_chrono_days, hourly_breakdown, dark_mode)
        #Graph.fetches(sorted_hourly_breakdown)
        #Graph.pushes(sorted_hourly_breakdown)
        #Graph.ref_ads(sorted_hourly_breakdown)
        #Graph.shallow_clones(sorted_hourly_breakdown)
        #Graph.summary(sorted_hourly_breakdown)
        #Graph.max_connections(sorted_hourly_breakdown)
        #Graph.protocols(sorted_hourly_breakdown)

        #Graph.repos(system_stats['repo_stats'], dark_mode)
        Graph.operations(system_stats['operations'], dark_mode)

        return("Dry Run complete")
        #return(path_to_completed_pdf)


    def sort_days(hourly_breakdown_keys):
        # list all days in chronoligical order
        all_chrono_days = list(hourly_breakdown_keys)
        all_chrono_days.sort()
        return all_chrono_days

    def clones(all_chrono_days, hourly_breakdown, dark_mode):
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

        plt.figure(figsize=(24,10))
        plt.subplots_adjust(top=0.96, bottom=0.05, left=0.04, right=0.99, wspace=0.9)
        # bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.01,0.05)
        textprops={'color': 'black'}
        if dark_mode:
            textprops = {'color': 'w'}
            plt.style.use('dark_background')
        plt.plot(date_labels, clone_all_data, 'b--', label="Clone") 
        plt.plot(date_labels, clone_hit_data, 'g.-', label="Clone/Cache Hit")
        plt.plot(date_labels, clone_miss_data, 'r.-', label="Clone/Cache Miss")
        #plt.plot([], operation], labels=labels, textprops=textprops)
        plt.title("Clone Operations", fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.xlabel('')
        plt.legend()
        plt.xticks(date_labels[::24])
        plt.ylabel('Number of Clones', fontdict={'fontweight': 'bold', 'fontsize': 14})

        plt.savefig('clones.png')

    def fetches(hourly_breakdown):
        pass

    def pushes(hourly_breakdown):
        pass

    def ref_ads(hourly_breakdown):
        pass

    def shallow_clones(hourly_breakdown):
        pass

    def summary(hourly_breakdown):
        pass

    def max_connections(hourly_breakdown):
        pass

    def protocols(hourly_breakdown):
        pass

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
        # Per repository
        #for repo_identifier in repo_stats:
            
        #plt.title(f"")
        #labels = [""]


    def operations(operations, dark_mode):
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
            textprops = {'color': 'w'}
            plt.style.use('dark_background')
        
        labels = ["git http", "git ssh", "rest", "web_ui", "filesystem"]
        plt.pie([operations['git_http'], operations['git_ssh'], operations['rest'], operations['web_ui'], operations['filesystem']], labels=labels, textprops=textprops)
        plt.title("Distribution of Operations")
        plt.xlabel('')
        plt.ylabel('')
        plt.savefig('operations.png')






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
