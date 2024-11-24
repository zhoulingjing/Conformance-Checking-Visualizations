import pm4py
import pandas
from sklearn.model_selection import train_test_split
import os


def conformance(file_path):
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)

    elif type[1] == '.csv':
        event_log = pandas.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name', activity_key='concept:name',
                                           timestamp_key='time:timestamp')

    case_ids = event_log['case:concept:name'].unique()  # split data into test and training data
    train_ids, test_ids = train_test_split(case_ids, test_size=0.99, random_state=42)
    train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
    test_log = event_log[event_log['case:concept:name'].isin(test_ids)]

    model, im, fm = pm4py.discover_petri_net_inductive(train_log)  # process discovery
    pm4py.view_petri_net(model, im, fm)

    for id in test_log['case:concept:name'].unique():
        log = test_log[test_log['case:concept:name'] == id]
        diagnostics = pm4py.conformance_diagnostics_token_based_replay(log, model, im,
                                                                       fm)  # for each case calculate the fitness
        conformance = diagnostics[0]
        print(f"{id} Conformance is {conformance['trace_fitness']}")


conformance('receipt.csv')