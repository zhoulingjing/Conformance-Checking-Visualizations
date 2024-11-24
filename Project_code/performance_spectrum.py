
import pm4py
import pandas as pd
import os

# def extract_activities(event_log):
#     activities = list(event_log['concept:name'].unique())
#     return activities


def convert_to_list(activity_input):
    return list(activity_input.split(","))


def generate_performance_spectrum(file_path):
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)
        event_log['time:timestamp'] = pd.to_datetime(event_log['time:timestamp']).dt.round('H')
        vars = pm4py.get_variants(event_log)
        variant_number = max(vars, key=vars.get)
        activities = list(variant_number)
        try:
            pm4py.view_performance_spectrum(event_log,activities, format="png")
        except Exception as e:
            print('Failed to generate the performance spectrum: ',e)

    elif type[1] == '.csv':
        event_log = pd.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case_id',activity_key='Activity',timestamp_key='time:timestamp')
        vars = pm4py.get_variants(event_log)
        variant_number = max(vars, key=vars.get)
        activities = list(variant_number)
        try:
            pm4py.view_performance_spectrum(event_log,activities, format="png")
        except Exception as e:
            print('Failed to generate the performance spectrum: ',e)




generate_performance_spectrum('Project_code/receipt.xes')