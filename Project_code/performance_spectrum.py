import pm4py
import pandas
import os


def generate_performance_spectrum(file_path):
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)
        vars = pm4py.get_variants(event_log)
        variant_number = max(vars, key=vars.get)
        activities = list(variant_number)
        try:
            pm4py.view_performance_spectrum(event_log, activities ,format="png")
        except Exception as e:
            print('Failed to generate the performance spectrum: ',e)

    elif type[1] == '.csv':
        event_log = pandas.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name',activity_key='concept:name',timestamp_key='time:timestamp')
        vars = pm4py.get_variants(event_log)
        variant_number = max(vars, key=vars.get)
        activities = list(variant_number)
        try:
            pm4py.view_performance_spectrum(event_log,activities, format="png")
        except Exception as e:
            print('Failed to generate the performance spectrum: ',e)




