import pm4py
import pandas
import os

def generate_performance_spectrum(file_path, activities):
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)
        try:
            pm4py.view_performance_spectrum(event_log,activities, format="png")
        except Exception as e:
            print('Failed to generate the performance spectrum: ',e)

    elif type[1] == '.csv':
        event_log = pandas.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case_id',activity_key='Activity',timestamp_key='time:timestamp')
        try:
            pm4py.view_performance_spectrum(event_log,activities, format="png")
        except Exception as e:
            print('Failed to generate the performance spectrum: ',e)



generate_performance_spectrum('running-example.xes',['register request', 'examine casually'])