import pm4py
from import_t import import_csv
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from sklearn.model_selection import train_test_split
import pandas
import os


def convert_to_event_log(file_path): 
        type = os.path.splitext(file_path)
        if type[1] == '.xes':
            event_log = pm4py.read_xes(file_path)
    
        elif type[1] == '.csv':
            event_log = pandas.read_csv(file_path)
            event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name',activity_key='concept:name',timestamp_key='time:timestamp')

        return event_log
        
#Generates a dotted chart
def generate_dotted_chart(file_path):
    event_log = convert_to_event_log(file_path)
    try:
        pm4py.view_dotted_chart(event_log, format="png", bgcolor="white", show_legend=True)
        print("Dotted chart.")
    except Exception as e:
        print("Failed to generate the dotted chart:", e)


#Generates a Petri net
def generate_petri_net(file_path):
    event_log = convert_to_event_log(file_path)
    try:
        net, im, fm = pm4py.discover_petri_net_inductive(event_log, activity_key='concept:name',
                                                         case_id_key='case:concept:name',
                                                         timestamp_key='time:timestamp')
        pm4py.view_petri_net(net, im, fm, format='png')
        print("PETRI_NETZ.")
    except Exception as e:
        print("Failed to generate the PETRI_NET chart:", e)


#Generates a dotted chart
def generate_process_tree(file_path):
    event_log = convert_to_event_log(file_path)
    try:
        process_tree = pm4py.discover_process_tree_inductive(event_log)
        bpmn_model = pm4py.convert_to_bpmn(process_tree)
        pm4py.view_bpmn(bpmn_model)
    except Exception as e:
        print("Failed to generate the process_tree chart:", e)


def split_data(file_path):
    event_log = convert_to_event_log(file_path)
    case_ids = event_log['case:concept:name'].unique()  # split data into test and training data
    train_ids, test_ids = train_test_split(case_ids, test_size=0.1, random_state=42)
    train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
    test_log = event_log[event_log['case:concept:name'].isin(test_ids)]
    return train_log, test_log


