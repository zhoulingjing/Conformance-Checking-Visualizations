import pm4py
from import_t import import_csv
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.filtering.pandas import timestamp_filter



def generate_dotted_chart(event_log):

    try:
        pm4py.view_dotted_chart(event_log, format="png", bgcolor= "white",show_legend=True)
        print("Dotted chart.")
    except Exception as e:
        print("Failed to generate the dotted chart:", e)


def generate_petri_netz(event_log):
    try:
        net, im, fm = pm4py.discover_petri_net_inductive(event_log, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')
        pm4py.view_petri_net(net, im, fm, format='png')
        print("PETRI_NETZ.")
    except Exception as e:
        print("Failed to generate the PETRI_NET chart:", e)


def generate_process_tree(event_log):

    try:
        process_tree = pm4py.discover_process_tree_inductive(event_log)
        bpmn_model = pm4py.convert_to_bpmn(process_tree)
        pm4py.view_bpmn(bpmn_model)
    except Exception as e:
        print("Failed to generate the process_tree chart:", e)


if __name__ == "__main__":

    file_path = r"E:\Conformance-Checking-Visualizations\Project_code\running-example.csv"

    event_log = import_csv(file_path)

    #process tree 
    generate_process_tree(event_log)
    #Petri_netz
    generate_petri_netz(event_log)
    #Dotted_chart
    generate_dotted_chart(event_log)