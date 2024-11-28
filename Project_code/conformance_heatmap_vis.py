import pm4py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split

# Function to generate conformance heatmap with concept drift over time
def generate_conformance_heatmap_with_time(file_path, coloring='YlGnBu', pnml_path=None):
    """
    file_path: file path to the log file
    coloring: colouring for the heatmap
    pnml_path=path of the pnml model by default is None
    
    """
    try:
        # Reading the XES file
        log = pm4py.read_xes(file_path)
        print("Parsing log...")

        # Step 1: Split the log into training and testing sets
        train_log, test_log = train_test_split(log, test_size=0.3, random_state=42)  # 30% for testing
        
        print(f"Train log size: {len(train_log)} traces")
        print(f"Test log size: {len(test_log)} traces")
        net, initial_marking, final_marking =None,None,None
        # Step 2: Discover the Petri net model using the inductive miner on the training log
        if pnml_path == None:
            net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(train_log)
        else:
            net, initial_marking, final_marking= pm4py.read.read_pnml(pnml_path)
        
        # Step 3: Replay the training log using the Petri net (this returns a replay result for conformance checking)
        replay_result_train = pm4py.conformance_diagnostics_alignments(train_log, net, initial_marking, final_marking)

        # Step 4: Replay the test log using the same Petri net (this returns a replay result for conformance checking)
        replay_result_test = pm4py.conformance_diagnostics_alignments(test_log, net, initial_marking, final_marking)

        # Initialize a list to store the transition counts and conformance over time
        time_series_train = []
        time_series_test = []

        # Step 5: Process the training log for conformance over time
        for trace_diagnostics in replay_result_train:
            alignment = trace_diagnostics['alignment']
            time_series_for_trace = []
           
            matches=0
            iterations=0
            for step in alignment:
                log_activity, replayed_activity = step
                iterations += 1
                # Calculate conformance score
                if log_activity and replayed_activity:
                    if log_activity == replayed_activity:
                        matches+=1
                    
                '''else:
                    conformance_score = 0.3  # No alignment found, lower score'''
                conformance_score=matches/iterations
                time_series_for_trace.append(conformance_score)
            time_series_train.append(time_series_for_trace)


        # Step 6: Process the test log for conformance over time
        for trace_diagnostics in replay_result_test:
            alignment = trace_diagnostics['alignment']
            time_series_for_trace = []
            matches=0
            iterations=0
            for step in alignment:
                log_activity, replayed_activity = step
                iterations += 1
                # Calculate conformance score
                if log_activity and replayed_activity:
                    if log_activity == replayed_activity:
                        matches+=1

                conformance_score=matches/iterations
                time_series_for_trace.append(conformance_score)
            time_series_test.append(time_series_for_trace)

        # Convert time series lists to DataFrames for easy visualization
        time_df_train = pd.DataFrame(time_series_train)
        time_df_test = pd.DataFrame(time_series_test)

        # Now generate the heatmap for training and testing logs
        plt.figure(figsize=(12, 8))

        # Plot for training log
        plt.subplot(1, 2, 1)
        sns.heatmap(time_df_train, annot=False, cmap=coloring, cbar=True, xticklabels=True, yticklabels=True)
        plt.title("Conformance Heatmap (Training Set)")
        plt.xlabel("Event Time Step")
        plt.ylabel("Trace ID")

        # Plot for test log
        plt.subplot(1, 2, 2)
        sns.heatmap(time_df_test, annot=False, cmap=coloring, cbar=True, xticklabels=True, yticklabels=True)
        plt.title("Conformance Heatmap (Test Set)")
        plt.xlabel("Event Time Step")
        plt.ylabel("Trace ID")

        # Display the heatmap
        plt.tight_layout()
       #plt.show()
        plt.savefig('../images/chcd.png')


    except Exception as e:
        print(f"Error generating conformance heatmap: {e}")

# Example usage:
generate_conformance_heatmap_with_time('./running-example.xes',"jet")