import pm4py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split


def get_unique_variants(event_log):
    traces = []
    vars = pm4py.get_variants(event_log)
    for trace in vars:
        traces.append(trace)
    return traces


# Function to generate conformance heatmap with concept drift over time
def generate_conformance_heatmap_with_time(file_path):
    try:
        # Reading the XES file
        event_log = pm4py.read_xes(file_path)
        print("Parsing log...")

        # Step 1: Split the log into training and testing sets
        case_ids = event_log['case:concept:name'].unique()  # split data into test and training data
        train_ids, test_ids = train_test_split(case_ids, test_size=0.5, random_state=42)
        train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
        test_log = event_log[event_log['case:concept:name'].isin(test_ids)]
        traces = get_unique_variants(test_log)
        model, im, fm = pm4py.discover_petri_net_inductive(train_log)
        # model, im, fm = pm4py.read_pnml('Testing/model.pnml')
        # test_log = event_log

        time_series_train = []

        for trace in traces:
            subset_trace = []
            time_series_for_trace = []
            print(trace)
            test_log_filtered = pm4py.filtering.filter_variants(test_log, [trace])
            for activity in trace:
                subset_trace.append(activity)
                test_log_filtered2 = pm4py.filtering.filter_event_attribute_values(test_log_filtered,
                                                                                   attribute_key='concept:name',
                                                                                   values=subset_trace, level='event')
                fitness = pm4py.fitness_token_based_replay(test_log_filtered2, model, im, fm)
                conformance_score = fitness['average_trace_fitness']
                time_series_for_trace.append(conformance_score)
                print(conformance_score)
            time_series_train.append(time_series_for_trace)

        # Convert time series lists to DataFrames for easy visualization
        time_df_train = pd.DataFrame(time_series_train)

        # Now generate the heatmap for training and testing logs
        plt.figure(figsize=(12, 8))

        # Plot for training log
        sns.heatmap(time_df_train, annot=False, cmap="YlGnBu", cbar=True, xticklabels=True, yticklabels=True)
        num_columns = time_df_train.shape[1]
        plt.xticks(ticks=np.arange(num_columns) + 0.5, labels=np.arange(1, num_columns + 1))
        plt.title("Conformance Heatmap")
        plt.xlabel("Steps in Trace")
        plt.ylabel("Trace ID")

        # Display the heatmap
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error generating conformance heatmap: {e}")


# Example usage:
generate_conformance_heatmap_with_time("Testing/running-example.xes")