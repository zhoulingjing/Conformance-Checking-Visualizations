#TO BE IMPLEMENTED
import os
import pandas as pd
import pm4py
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

'''
The code processes the event log to extract the sequence of activities (concept:name) for each case_id.
By iterating through the activity sequences, the code determines direct transitions (order of activities).
The code calculates the frequency of each transition across all cases and uses it to set edge thickness in the visualization.

Nodes are created for all unique activities in the event log (extracted from the concept:name column).
Directed edges are added to represent transitions between activities, determined from the sequential flow of each case in the event log.

Edge thickness:
The thickness of edges is proportional to the frequency of transitions between activities.
This allows users to identify the most common paths in the process.
Edge color:
(We still don't get the comfarmance score)

The network highlights the relationships between activities (via edges) and the prominence of activities (via node size).
'''

def convert_to_event_log(file_path): 
    """
    Converts the given file (XES or CSV) into an event log.
    """
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)
    
    elif type[1] == '.csv':
        event_log = pd.read_csv(file_path)
        event_log = pm4py.format_dataframe(
            event_log, 
            case_id='case:concept:name',
            activity_key='concept:name',
            timestamp_key='time:timestamp'
        )
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xes file.")
    
    return event_log


def build_activity_network(log):
    """
    Creates an interaction network from the event log.
    """
    interaction_network = nx.DiGraph()

    if isinstance(log, pd.DataFrame):
        grouped_cases = log.groupby('case:concept:name')
    else:
        grouped_cases = log

    for _, trace in grouped_cases:
        prev_activity = None
        for _, event in trace.iterrows():
            current_activity = event['concept:name']
            if prev_activity:
                if interaction_network.has_edge(prev_activity, current_activity):
                    interaction_network[prev_activity][current_activity]['count'] += 1
                else:
                    interaction_network.add_edge(prev_activity, current_activity, count=1)
            prev_activity = current_activity

    return interaction_network


def visualize_interaction_graph(activity_network):
    """
    Visualizes the activity interaction network with customized styling.
    """
    plt.figure(figsize=(12, 10))

    # Layout setup
    layout = nx.random_layout(activity_network)  # Random layout for a distinct visual style

    # Node properties
    node_strengths = [activity_network.degree(n, weight='count') for n in activity_network.nodes]
    node_sizes = [600 + 80 * s for s in node_strengths]
    node_colors = node_strengths
    cmap = LinearSegmentedColormap.from_list("custom_gradient", ["#A7C7E7", "#00274D"], N=100)

    # Edge properties
    edge_weights = nx.get_edge_attributes(activity_network, 'count')
    edge_colors = [w for w in edge_weights.values()]

    # Draw graph
    nodes = nx.draw_networkx_nodes(
        activity_network,
        pos=layout,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=cmap
    )
    nx.draw_networkx_edges(
        activity_network,
        pos=layout,
        edge_color=edge_colors,
        edge_cmap=plt.cm.Greens,
        width=2.0
    )
    nx.draw_networkx_labels(
        activity_network,
        pos=layout,
        font_color='black',
        font_weight='bold'
    )

    # Add color bar for nodes
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_strengths), vmax=max(node_strengths)))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.85)
    cbar.set_label('Node Strength (Degree)', fontsize=12)

    # Show the graph instead of saving
    plt.title("Customized Activity Interaction Network", fontsize=16, color="darkgreen", fontweight="bold")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # Specify the input file path
    input_path = r"D:\Final\Conformance-Checking-Visualizations\Final_Code\running-example.xes"

    try:
        # Convert the file to an event log
        event_log = convert_to_event_log(input_path)

        # Build the activity interaction network
        interaction_network = build_activity_network(event_log)

        # Visualize and save the interaction graph
        visualize_interaction_graph(interaction_network)

<<<<<<< Updated upstream
    except Exception as err:
        print("Error:", err)
=======
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
#file_path = "Final_Code/running-example.xes"  # Update with your XES or CSV file path
#generate_activity_interaction_network_with_edge_fitness(file_path)
>>>>>>> Stashed changes
