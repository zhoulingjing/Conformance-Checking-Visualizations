import pm4py


def generate_dotted_chart(event_log):
    try:
        pm4py.view_dotted_chart(event_log, format="png", bgcolor="white", show_legend=True)
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
    file_path = "Project_code/running-example.xes"  


    event_log = pm4py.read_xes(file_path)  

    # Process tree 
    generate_process_tree(event_log)

    # Petri net
    generate_petri_netz(event_log)

    # Dotted chart
    generate_dotted_chart(event_log)

