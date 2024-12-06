import pm4py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split


def get_unique_variants(event_log):
    """Extract unique variants from the event log."""
    variants = pm4py.get_variants(event_log)
    print(f"Found {len(variants)} variants")
    return variants


def abbreviate_activities(list_of_activities):
    """Abbreviate activity names for readability in the heatmap."""
    final_word = ''
    for activity in list_of_activities:
        words = activity.split()
        abbreviation = words[0] + (words[1][:3].capitalize() if len(words) > 1 else '')
        final_word += abbreviation + '-'
    return final_word[:-1]


def load_event_log(file_path):
    """Load the event log from CSV or XES file."""
    ext = file_path.split('.')[-1].lower()
    if ext == 'xes':
        return pm4py.read_xes(file_path)
    elif ext == 'csv':
        df = pd.read_csv(file_path)
        required_columns = ['case:concept:name', 'concept:name', 'time:timestamp']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV file must contain columns: {', '.join(required_columns)}")
        df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], errors='coerce')
        if df['time:timestamp'].isnull().any():
            print("Warning: Dropping rows with invalid timestamps.")
            df = df.dropna(subset=['time:timestamp'])
        return pm4py.format_dataframe(df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def generate_conformance_heatmap_with_time(file_path, coloring='YlGnBu', pnml_path=None, time_granularity='M'):
    """Generate conformance heatmaps with concept drift analysis over time."""
    try:
        # Load the event log
        event_log = load_event_log(file_path)
        event_log['time:timestamp'] = pd.to_datetime(event_log['time:timestamp'])
        event_log['time_slice'] = event_log['time:timestamp'].dt.to_period(time_granularity)

        time_slice_heatmaps = {}

        # Process each time slice
        for time_slice, slice_log in event_log.groupby('time_slice'):
            print(f"Processing time slice: {time_slice}")

            # Split the log into training and testing sets
            case_ids = slice_log['case:concept:name'].unique()
            train_ids, test_ids = train_test_split(case_ids, test_size=0.45, random_state=42)
            train_log = slice_log[slice_log['case:concept:name'].isin(train_ids)]
            test_log = slice_log[slice_log['case:concept:name'].isin(test_ids)]
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

            # Generate the heatmap for this time slice
            plt.figure(figsize=(12, 8))
            sns.heatmap(
                time_df_train,
                annot=False,
                cmap=coloring,
                cbar=True,
                xticklabels=True,
                yticklabels=y_axis_labels
            )
            plt.title(f"Conformance Heatmap - {time_slice}")
            plt.xlabel("Steps in Trace")
            plt.ylabel("Trace ID")

            num_columns = time_df_train.shape[1]
            plt.xticks(ticks=np.arange(num_columns) + 0.5, labels=np.arange(1, num_columns + 1))

            plt.tight_layout()

            output_folder = './Final_Code/output_images'
            output_path = f"{output_folder}/heatmap_{time_slice}.png"
            plt.savefig(output_path)
            plt.show()

            time_slice_heatmaps[time_slice] = output_path

        return time_slice_heatmaps

    except Exception as e:
        print(f"Error generating conformance heatmap: {e}")
        return None

