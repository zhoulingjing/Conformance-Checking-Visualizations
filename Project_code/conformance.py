import pm4py
import os
import pandas
from sklearn.model_selection import train_test_split
def conformance(event_log,conformance_algorithm=None,model_path=None):
    if conformance_algorithm==None and model_path==None:
        conformance_log(event_log)
        return
    
    model=[]
    if model_path!=None:
        type=os.path.splitext(model_path)
        
        if type[1]==".pnml":
            model = pm4py.read.read_pnml(model_path)
        elif type[1]==".bpmn":
            model[0] = pm4py.read_bpmn(model_path)
        elif type[1]==".dfg":
            model[0] =pm4py.read_dfg(model_path)
        elif type[1]=="ptml":
            model[0]= pm4py.read_ptml(model_path)
        else:
            raise TypeError
        
    if conformance_algorithm!=None:
        if conformance_algorithm=='conformance_diagnostics_alignments' or conformance_algorithm=='conformance diagnostics alignments' or conformance_algorithm=='cda':
            pm4py.conformance.conformance_diagnostics_alignments(event_log,model)
        elif conformance_algorithm == 'conformance_diagnostics_token_based_replay' or conformance_algorithm == 'conformance diagnostics token based replay' or conformance_algorithm=='cdtbr':
            pm4py.conformance_diagnostics_token_based_replay(event_log, model)
    
        
    
    
def conformance_log(event_log):
    event_log = pandas.read_csv('receipt.csv')
    event_log = pm4py.format_dataframe(event_log,case_id='case:concept:name', activity_key='concept:name',timestamp_key='time:timestamp')

    case_ids = event_log['case:concept:name'].unique()                                  #split data into test and training data
    train_ids,test_ids = train_test_split(case_ids, test_size= 0.999, random_state= 42)
    train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
    test_log = event_log[event_log['case:concept:name'].isin(test_ids)]

    model, im, fm = pm4py.discover_petri_net_inductive(train_log)   #process discovery
    pm4py.view_petri_net(model,im,fm)


    for id in test_log['case:concept:name'].unique():
        log = test_log[test_log['case:concept:name'] == id]
        dict = pm4py.conformance_diagnostics_token_based_replay(log,model,im,fm)       #for each case calculate the fitness
        conformance = dict[0]
        print(f"{id} Conformance is {conformance['trace_fitness']}")

conformance('d')
