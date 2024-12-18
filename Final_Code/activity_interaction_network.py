import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pm4py
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
import os


def convert_to_event_log(file_path):
    """Convert a file (XES or CSV) to a PM4Py event log format."""
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.xes':
        event_log = pm4py.read_xes(file_path)
    elif file_extension == '.csv':
        event_log = pd.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name', activity_key='concept:name',
                                           timestamp_key='time:timestamp')
    return event_log


def calc_frequency(event_log):
    """Calculate the frequency of each activity in the event log."""
    frequencies = {}
    for activity in event_log['concept:name']:
        if activity in frequencies.keys():
            frequencies[activity] += 1
        else:
            frequencies.update({activity: 1})
    return frequencies


def extract_activity_transitions(event_log):
    """Extract transitions (edges) between activities from the event log."""
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
    """Generate the Activity Interaction Network (AIN) from the event log."""
    transitions = extract_activity_transitions(event_log)
    activity_frequencies = calc_frequency(event_log)

    G = nx.DiGraph()

    for activity, frequency in activity_frequencies.items():
        G.add_node(activity, frequency=frequency)

    for _, row in transitions.iterrows():
        G.add_edge(row["source"], row["target"], frequency=row["frequency"])

    return G


def map_edge_fitness_to_color(edge_fitness_scores):
    """Map fitness scores to edge colors based on fitness values."""
    if not edge_fitness_scores:
        return {}  # If no edge fitness scores, return an empty dictionary

    cmap = plt.colormaps.get_cmap("plasma")  # Use vibrant colormap
    norm = plt.Normalize(vmin=min(edge_fitness_scores.values()), vmax=max(edge_fitness_scores.values()))
    return {(source, target): cmap(norm(score)) for (source, target), score in edge_fitness_scores.items()}


def calculate_edge_fitness(longest_trace, model, im, fm):
    """Calculate fitness for each edge in the activity interaction network."""
    edge_fitness_scores = {}

    # Ensure that the longest_trace contains at least two activities for transitions
    if len(longest_trace) < 2:
        print("Warning: The longest trace has fewer than two activities.")
        return edge_fitness_scores

    # For each transition between activities, calculate fitness
    for i in range(len(longest_trace) - 1):
        source = longest_trace.iloc[i]["concept:name"]
        target = longest_trace.iloc[i + 1]["concept:name"]

        try:
            edge_trace = longest_trace[
                (longest_trace["concept:name"] == source) | (longest_trace["concept:name"] == target)]
            alignment_result = alignments.apply(edge_trace, model, im, fm)
            fitness = alignment_result[0]["fitness"]
            edge_fitness_scores[(source, target)] = fitness
        except Exception as e:
            print(f"Error calculating edge fitness for {source} -> {target}: {e}")
            edge_fitness_scores[(source, target)] = 0  # Assign default fitness value of 0 in case of error

    return edge_fitness_scores


def visualize_activity_interaction_network_with_edge_fitness(G, edge_fitness_scores):
    """Visualize the Activity Interaction Network with fitness-based coloring on edges."""
    fig, ax = plt.subplots(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.3, seed=42)
    node_sizes = [G.nodes[node]["frequency"] * 50 for node in G.nodes]
    edge_widths = [G[u][v]["frequency"] * 1.2 for u, v in G.edges()]

    # Node visualization
    nx.draw_networkx_nodes(
        G, pos, node_size=node_sizes, node_color="lightblue", alpha=0.9, ax=ax
    )

    # Edge visualization with fitness-based color
    edge_colors = [edge_fitness_scores.get((u, v), "gray") for u, v in G.edges()]
    nx.draw_networkx_edges(
        G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.7, ax=ax
    )

    # Node labels
    nx.draw_networkx_labels(
        G, pos, font_size=12, font_color="darkblue", font_weight="bold", ax=ax
    )

    # Create a color bar for edge fitness scores
    sm = plt.cm.ScalarMappable(cmap="plasma", norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Edge Fitness", fontsize=14)

    ax.set_title("Activity Interaction Network with Edge-Level Conformance (Fitness)", fontsize=16)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig('./Final_Code/output_images/ain_with_edge_fitness.png')
    plt.show()


def extract_longest_trace(event_log):
    """Extract the longest trace from the event log."""
    grouped = event_log.groupby("case:concept:name")
    trace_lengths = grouped.size()
    longest_trace_case = trace_lengths.idxmax()
    longest_trace = grouped.get_group(longest_trace_case)
    return longest_trace


# Main function to generate the Activity Interaction Network with edge-level fitness coloring
def generate_activity_interaction_network_with_edge_fitness(file_path):
    """
    Generate an Activity Interaction Network (AIN) with edge fitness-based coloring.
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

        # Calculate fitness for edges
        edge_fitness_scores = calculate_edge_fitness(longest_trace, model, im, fm)

        # If no edge fitness scores are calculated, print a message
        if not edge_fitness_scores:
            print("No edge fitness scores were calculated. Ensure the transitions are valid.")

        # Map edge fitness to colors
        edge_colors = map_edge_fitness_to_color(edge_fitness_scores)

        # Visualize the Activity Interaction Network with edge fitness coloring
        visualize_activity_interaction_network_with_edge_fitness(ain_graph, edge_colors)

    except Exception as e:
        print(f"Error in generating AIN with edge fitness: {e}")

# Example usage:
# file_path = "Final_Code/running-example.xes"  # Update with your XES or CSV file path
# generate_activity_interaction_network_with_edge_fitness(file_path)