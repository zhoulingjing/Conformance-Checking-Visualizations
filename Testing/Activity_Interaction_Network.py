import pandas
import pm4py
import networkx as nx
import matplotlib.pyplot as plt

def get_unique_activities(event_log):
    return list(set(event_log['concept:name']))

def generate_ain(event_log):
    """Generate an Activity Interaction Network (AIN) with node sizes adjusted to fit labels."""
    # Get unique activities
    unique_activities = get_unique_activities(event_log)

    # Create the graph
    G = nx.Graph()
    for activity in unique_activities:
        G.add_node(activity)

    # Determine node sizes based on activity label lengths
    # Multiply by a scaling factor to ensure enough space
    scaling_factor = 500  # Adjust as needed for aesthetics
    node_sizes = [len(activity) * scaling_factor for activity in unique_activities]

    # Draw the graph
    plt.figure(figsize=(10, 10))
    nx.draw_networkx(
        G,
        node_size=node_sizes,  # Adjust node sizes
        with_labels=True,
        font_size=10,
        node_color="skyblue",
        edge_color="gray"
    )
    plt.title("Activity Interaction Network (AIN)")
    plt.show()

event_log = pm4py.read_xes('Testing/running-example.xes')
generate_ain(event_log)