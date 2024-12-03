import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from import_t import import_csv

def calc_frequency(event_log):
    frequencies = {}
    for activity in event_log['concept:name']:
        if activity in frequencies.keys():
            frequencies[activity] += 1
        else:
            frequencies.update({activity: 1})
    return frequencies



def get_unique_activities(event_log):

    return list(set(event_log['concept:name']))


def extract_activity_transitions(event_log):

    transitions = []
    grouped = event_log.groupby("case:concept:name")
    for _, group in grouped:
        sorted_group = group.sort_values("time:timestamp")
        activities = sorted_group["concept:name"].tolist()
        transitions += [(activities[i], activities[i + 1]) for i in range(len(activities) - 1)]

    transition_df = pd.DataFrame(transitions, columns=["source", "target"])
    transition_df = transition_df.groupby(["source", "target"]).size().reset_index(name="frequency")
    return transition_df


def generate_activity_interaction_network(event_log):

    transitions = extract_activity_transitions(event_log)
    activity_frequencies = calc_frequency(event_log)


    G = nx.DiGraph()

    for activity, frequency in activity_frequencies.items():
        G.add_node(activity, frequency=frequency)

    for _, row in transitions.iterrows():
        G.add_edge(row["source"], row["target"], frequency=row["frequency"])

    return G


def visualize_activity_interaction_network(G):

    plt.figure(figsize=(12, 8))

    node_sizes = [G.nodes[node]["frequency"] * 50 for node in G.nodes]


    edge_widths = [G[u][v]["frequency"] / 2 for u, v in G.edges]


    edge_colors = "black"
    #we can add different colors for the edges later


    pos = nx.spring_layout(G, seed=42)


    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue", alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="blue")

    plt.title("Activity Interaction Network (AIN)")
    plt.axis("off")

    plt.show()



def extract_longest_trace(event_log):

    grouped = event_log.groupby("case:concept:name")
    trace_lengths = grouped.size()

    longest_trace_case = trace_lengths.idxmax()

    longest_trace = grouped.get_group(longest_trace_case)
    return longest_trace




file_path = "running-example.csv"
event_log = pd.read_csv(file_path)


event_log["time:timestamp"] = pd.to_datetime(event_log["time:timestamp"], utc=True)


longest_trace = extract_longest_trace(event_log)


ain_graph = generate_activity_interaction_network(longest_trace)


visualize_activity_interaction_network(ain_graph)