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
def abbreviate_activities(list_of_activities):
    final_word=''
    for activity in list_of_activities:
        final_word+="".join(e[0] for e in activity.split())
        final_word+='-'
        
    return final_word[:-1]

# Function to generate conformance heatmap with concept drift over time
def generate_conformance_heatmap_with_time(file_path, coloring='YlGnBu', pnml_path=None):
    """
    file_path: file path to the log file
    coloring: colouring for the heatmap
    pnml_path=path of the pnml model by default is None
    
    """
    try:
        # Reading the XES file
        event_log = pm4py.read_xes(file_path)
        # Step 1: Split the log into training and testing sets
        case_ids = event_log['case:concept:name'].unique()  # split data into test and training data
        train_ids, test_ids = train_test_split(case_ids, test_size=0.5, random_state=42)
        train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
        test_log = event_log[event_log['case:concept:name'].isin(test_ids)]
        traces = get_unique_variants(test_log)
        if pnml_path==None:
            model, im, fm = pm4py.discover_petri_net_inductive(train_log) 
        else:
            model, im, fm = pm4py.read_pnml(pnml_path)
        # test_log = event_log

        time_series_train = []
        y_axis_labels = [] 
        for trace in traces:
            subset_trace = []
            time_series_for_trace = []
            # print(trace)
            test_log_filtered = pm4py.filtering.filter_variants(test_log,[trace])
            for activity in trace:
                subset_trace.append(activity)
                test_log_filtered2 = pm4py.filtering.filter_event_attribute_values(test_log_filtered,attribute_key= 'concept:name', values=subset_trace,level='event')
                fitness = pm4py.fitness_token_based_replay(test_log_filtered2,model,im,fm)
                conformance_score = fitness['average_trace_fitness']
                time_series_for_trace.append(conformance_score)
                # print(conformance_score)
            y_axis=abbreviate_activities(subset_trace)
            print(y_axis)
            y_axis_labels.append(y_axis)
            time_series_train.append(time_series_for_trace)

        # Convert time series lists to DataFrames for easy visualization
        time_df_train = pd.DataFrame(time_series_train)

        # Now generate the heatmap for training and testing logs
        plt.figure(figsize=(12, 8))

        # Plot for training log
        sns.heatmap(time_df_train, annot=False, cmap=coloring, cbar=True, xticklabels=True, yticklabels=y_axis_labels)
        plt.title("Conformance Heatmap")
        plt.xlabel("Steps in Trace")
        plt.ylabel("Trace ID")


        # Display the heatmap
        plt.tight_layout()
        # plt.show()
        plt.savefig('./images/chcd.png')


    except Exception as e:
        print(f"Error generating conformance heatmap: {e}")

# Example usage:
generate_conformance_heatmap_with_time('/Users/aliraz/OneDrive - University College Dublin/RWTH Docs/2024/spp/final/Conformance-Checking-Visualizations/Project_code/running-example.xes',"jet")