"""
    Generates a performance spectrum visualization for the given event log.

    This function supports both XES and CSV file formats. It identifies the most frequent 
    variant of activities in the event log and generates a performance spectrum visualization. 
    The visualization is displayed in PNG format.

    Args:
        file_path (str): The file path of the event log (XES or CSV format).

    Steps:
        1. Determines the file type based on the extension.
        2. For XES files:
            - Reads the event log using PM4Py.
            - Extracts variants and selects the most frequent one.
            - Generates a performance spectrum visualization.
        3. For CSV files:
            - Reads the event log using pandas.
            - Formats it for PM4Py.
            - Extracts variants and selects the most frequent one.
            - Generates a performance spectrum visualization.
        4. Handles any exceptions during the visualization process.

    Notes:
        - If the performance spectrum cannot be generated, an error message is displayed.

"""
import os
import pandas as pd
import pm4py


def generate_performance_spectrum(file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    # Determine file type and read the event log
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)
    elif type[1] == '.csv':
        event_log = pd.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name',
                                           activity_key='concept:name',
                                           timestamp_key='time:timestamp')
    else:
        print("Unsupported file type. Please provide a .xes or .csv file.")
        return
    
    # Extract the most frequent variant
    try:
        variants = pm4py.get_variants(event_log)
        most_frequent_variant = max(variants, key=variants.get)
        activities = list(most_frequent_variant)
    except Exception as e:
        print("Failed to extract variants or activities:", e)
        return
    
    # Generate and save the performance spectrum
    try:
        output_path = os.path.join(output_dir, "performance_spectrum.png")
        pm4py.save_vis_performance_spectrum(event_log, activities, output_path)
        print(f"Performance spectrum saved to {output_path}.")
    except Exception as e:
        print("Failed to generate the performance spectrum:", e)
