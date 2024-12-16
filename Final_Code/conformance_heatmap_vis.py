import pm4py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split


def get_unique_variants(event_log):
    """Extract unique variants from the event log."""
    variants = pm4py.get_variants(event_log)
    print(f"Found {len(variants)} variants")  # Debugging: print number of variants
    return variants


def abbreviate_activities(list_of_activities):
    """Abbreviate activity names to make them more readable in the heatmap."""
    final_word = ''
    for activity in list_of_activities:
        words = activity.split()
        if len(words) > 1:
            abbreviation = words[0] + words[1][:3].capitalize()
        else:
            abbreviation = words[0]
        final_word += abbreviation + '-'
    return final_word[:-1]


def load_event_log(file_path):
    """Load the event log from CSV or XES file."""
    ext = file_path.split('.')[-1].lower()
    if ext == 'xes':
        return pm4py.read_xes(file_path)
    elif ext == 'csv':
        df = pd.read_csv(file_path)
        # Ensure the required columns are present in the CSV file
        required_columns = ['case:concept:name', 'concept:name', 'time:timestamp']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV file must contain the columns: {', '.join(required_columns)}")
        
        # Ensure 'time:timestamp' is in datetime format
        df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], errors='coerce')  # Handle invalid timestamps
        if df['time:timestamp'].isnull().any():
            print("Warning: Some timestamps could not be converted. Rows with invalid timestamps will be dropped.")
            df = df.dropna(subset=['time:timestamp'])  # Drop rows with invalid timestamps
        
        return pm4py.format_dataframe(df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def generate_conformance_heatmap_with_time(file_path, coloring='YlGnBu', pnml_path=None):
    """Generate conformance heatmap with concept drift over time."""
    try:
        # Load the event log
        event_log = load_event_log(file_path)

        # Split the log into training and testing sets
        case_ids = event_log['case:concept:name'].unique()
        train_ids, test_ids = train_test_split(case_ids, test_size=0.45, random_state=42)
        train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
        test_log = event_log[event_log['case:concept:name'].isin(test_ids)]
        traces = get_unique_variants(test_log)

        # Discover or read the Petri net model
        if pnml_path is None:
            model, im, fm = pm4py.discover_petri_net_inductive(train_log)
        else:
            model, im, fm = pm4py.read_pnml(pnml_path)

        # Initialize data for heatmap
        time_series_train = []
        y_axis_labels = []

        for trace in traces:
            subset_trace = []
            time_series_for_trace = []

            test_log_filtered = pm4py.filtering.filter_variants(test_log, [trace])
            for activity in trace:
                subset_trace.append(activity)
                test_log_filtered2 = pm4py.filtering.filter_event_attribute_values(
                    test_log_filtered, attribute_key='concept:name', values=subset_trace, level='event'
                )
                fitness = pm4py.fitness_token_based_replay(test_log_filtered2, model, im, fm)
                conformance_score = fitness['average_trace_fitness']
                time_series_for_trace.append(conformance_score)

            y_axis = abbreviate_activities(subset_trace)
            y_axis_labels.append(y_axis)
            time_series_train.append(time_series_for_trace)

        # Convert time series lists to DataFrame
        time_df_train = pd.DataFrame(time_series_train)

        # Generate the heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            time_df_train,
            annot=False,
            cmap=coloring,
            cbar=True,
            xticklabels=True,
            yticklabels=y_axis_labels
        )
        plt.title("Conformance Heatmap")
        plt.xlabel("Steps in Trace")
        plt.ylabel("Trace ID")

        num_columns = time_df_train.shape[1]
        plt.xticks(ticks=np.arange(num_columns) + 0.5, labels=np.arange(1, num_columns + 1))

        plt.tight_layout()
        
        plt.savefig('./Final_Code/output_images/chcd.png')
        plt.show()

    except Exception as e:
        print(f"Error generating conformance heatmap: {e}")
