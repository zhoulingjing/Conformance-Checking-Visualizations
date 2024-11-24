import pandas
import pm4py
import os

def generate_petri_net(file_path):
    type = os.path.splitext(file_path)
    
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)

    elif type[1] == '.csv':
        event_log = pandas.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case_id',activity_key='Activity',timestamp_key='time:timestamp')

    net, im, fm = pm4py.discover_petri_net_inductive(event_log)
    pm4py.view_petri_net(net,im,fm)


if __name__ == '__main__':
    generate_petri_net('running-example.xes')
