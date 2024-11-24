import pm4py
import pandas as pd
import os

def convert_to_list(activity_input):
    return list(activity_input.split(","))

# Custom function to round timestamps to desired granularity (hours, minutes, or seconds)
def custom_round_time(event_log, granularity="H"):
    """
    This function manually rounds the 'time:timestamp' field to the specified granularity.
    Granularity options: "H" for hour, "T" for minute, "S" for second
    """
    if granularity == "H":  # Hour rounding
        event_log['time:timestamp'] = pd.to_datetime(event_log['time:timestamp']).dt.floor('H')
    elif granularity == "T":  # Minute rounding
        event_log['time:timestamp'] = pd.to_datetime(event_log['time:timestamp']).dt.floor('T')
    elif granularity == "S":  # Second rounding
        event_log['time:timestamp'] = pd.to_datetime(event_log['time:timestamp']).dt.floor('S')
    else:
        raise ValueError("Unsupported granularity. Use 'H', 'T', or 'S'.")
    
    return event_log

# Function to generate the performance spectrum
def generate_performance_spectrum(file_path, granularity="H"):
    file_type = os.path.splitext(file_path)[1].lower()  # Get file extension
    if file_type == '.xes':
        # Read the XES file
        event_log = pm4py.read_xes(file_path)
        # Round timestamps as per the selected granularity
        event_log = custom_round_time(event_log, granularity)
        
        # Extract variants and activities
        vars = pm4py.get_variants(event_log)
        variant_number = max(vars, key=vars.get)
        activities = list(variant_number)
        
        # Generate and view the performance spectrum
        try:
            pm4py.view_performance_spectrum(event_log, activities, format="png")
        except Exception as e:
            print('Failed to generate the performance spectrum: ', e)

    elif file_type == '.csv':
        # Read the CSV file
        event_log = pd.read_csv(file_path)
        # Format the CSV into a proper event log for PM4Py
        event_log = pm4py.format_dataframe(event_log, case_id='case_id', activity_key='Activity', timestamp_key='time:timestamp')
        # Round timestamps as per the selected granularity
        event_log = custom_round_time(event_log, granularity)

        # Extract variants and activities
        vars = pm4py.get_variants(event_log)
        variant_number = max(vars, key=vars.get)
        activities = list(variant_number)
        
        # Generate and view the performance spectrum
        try:
            pm4py.view_performance_spectrum(event_log, activities, format="png")
        except Exception as e:
            print('Failed to generate the performance spectrum: ', e)

# Example usage
generate_performance_spectrum('Project_code/receipt.xes', granularity="H")  # You can set granularity to "T" or "S" for minutes or seconds
