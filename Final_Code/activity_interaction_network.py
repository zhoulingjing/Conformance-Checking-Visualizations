import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
import os

def convert_to_event_log(file_path): 
        type = os.path.splitext(file_path)
        if type[1] == '.xes':
            event_log = pm4py.read_xes(file_path)
    
        elif type[1] == '.csv':
            event_log = pd.read_csv(file_path)
            event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name',activity_key='concept:name',timestamp_key='time:timestamp')

        return event_log
        

def calc_frequency(event_log):
    frequencies = {}
    for activity in event_log['concept:name']:
        if activity in frequencies.keys():
            frequencies[activity] += 1
        else:
            frequencies.update({activity: 1})
    return frequencies

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

def map_fitness_to_color(fitness_scores):
    # Use a more vibrant color map like 'plasma' or 'coolwarm' for bolder colors
    cmap = plt.colormaps.get_cmap("plasma")
    norm = plt.Normalize(vmin=min(fitness_scores.values()), vmax=max(fitness_scores.values()))
    return {activity: cmap(norm(score)) for activity, score in fitness_scores.items()}

def visualize_activity_interaction_network(G, node_colors):
    fig, ax = plt.subplots(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.3, seed=42)
    node_sizes = [G.nodes[node]["frequency"] * 50 for node in G.nodes]
    edge_widths = [G[u][v]["frequency"] * 1.2 for u, v in G.edges()]
    
    nx.draw_networkx_nodes(
        G, pos, node_size=node_sizes, node_color=[node_colors.get(node, "gray") for node in G.nodes], 
        alpha=0.9, ax=ax
    )
    
    nx.draw_networkx_edges(
        G, pos, width=edge_widths, edge_color="black", alpha=0.7, ax=ax
    )
    
    nx.draw_networkx_labels(
        G, pos, font_size=12, font_color="darkblue", font_weight="bold", ax=ax
    )
    
    sm = plt.cm.ScalarMappable(cmap="plasma", norm=plt.Normalize(vmin=0, vmax=1))  # Adjusted color map
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Fitness", fontsize=14)
    
    ax.set_title("Activity Interaction Network (AIN) with Conformance-Based Coloring", fontsize=16)
    ax.axis("off")
    
    plt.tight_layout()
    plt.savefig('./Final_Code/ain.png')
    plt.show()

def extract_longest_trace(event_log):
    grouped = event_log.groupby("case:concept:name")
    trace_lengths = grouped.size()
    longest_trace_case = trace_lengths.idxmax()
    longest_trace = grouped.get_group(longest_trace_case)
    return longest_trace

file_path = "Final_Code/running-example.xes"
event_log = convert_to_event_log(file_path)

event_log["time:timestamp"] = pd.to_datetime(event_log["time:timestamp"], errors="coerce", utc=True)
event_log = event_log.dropna(subset=["time:timestamp"])
event_log["case:concept:name"] = event_log["case:concept:name"].astype(str)

longest_trace = extract_longest_trace(event_log)


train_log = longest_trace
model, im, fm = pm4py.discover_petri_net_inductive(train_log)

fitness_scores = {}
for activity in longest_trace["concept:name"].unique():
    activity_trace = longest_trace[longest_trace["concept:name"] == activity]
    try:
        alignment_result = alignments.apply(activity_trace, model, im, fm)
        fitness = alignment_result[0]["fitness"]
        fitness_scores[activity] = fitness
        print(f"Fitness for activity '{activity}': {fitness}")
    except Exception as e:
        print(f"Error calculating fitness for activity {activity}: {e}")
        fitness_scores[activity] = 0

node_colors = map_fitness_to_color(fitness_scores)


def generate_activity_interaction_network_with_fitness(file_path):
    """
    Generate an Activity Interaction Network (AIN) with fitness-based coloring.
    Accepts a file path that can be either a .csv or .xes log file.
    """
    try:
        # Convert the file to an event log
        event_log = convert_to_event_log(file_path)

        # Ensure timestamps are in the correct format and handle missing values
        event_log["time:timestamp"] = pd.to_datetime(event_log["time:timestamp"], errors="coerce", utc=True)
        event_log = event_log.dropna(subset=["time:timestamp"])
        event_log["case:concept:name"] = event_log["case:concept:name"].astype(str)

        # Extract the longest trace
        longest_trace = extract_longest_trace(event_log)

        # Generate Activity Interaction Network (AIN) graph
        ain_graph = generate_activity_interaction_network(longest_trace)

        # Discover Petri net model from the longest trace
        train_log = longest_trace
        model, im, fm = pm4py.discover_petri_net_inductive(train_log)

        # Calculate fitness scores for activities
        fitness_scores = {}
        for activity in longest_trace["concept:name"].unique():
            activity_trace = longest_trace[longest_trace["concept:name"] == activity]
            try:
                alignment_result = alignments.apply(activity_trace, model, im, fm)
                fitness = alignment_result[0]["fitness"]
                fitness_scores[activity] = fitness
                print(f"Fitness for activity '{activity}': {fitness}")
            except Exception as e:
                print(f"Error calculating fitness for activity {activity}: {e}")
                fitness_scores[activity] = 0

        # Map fitness scores to colors
        node_colors = map_fitness_to_color(fitness_scores)

        

        # Visualize the Activity Interaction Network
        visualize_activity_interaction_network(ain_graph, node_colors)
    
    except Exception as e:
        print(f"Error in generating AIN: {e}")





