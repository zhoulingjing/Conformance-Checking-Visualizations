import pm4py
from import_t import import_csv
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from sklearn.model_selection import train_test_split


def generate_dotted_chart(event_log):
    try:
        pm4py.view_dotted_chart(event_log, format="png", bgcolor="white", show_legend=True)
        print("Dotted chart.")
    except Exception as e:
        print("Failed to generate the dotted chart:", e)


def generate_petri_netz(event_log):
    try:
        net, im, fm = pm4py.discover_petri_net_inductive(event_log, activity_key='concept:name',
                                                         case_id_key='case:concept:name',
                                                         timestamp_key='time:timestamp')
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


def split_data(event_log):
    case_ids = event_log['case:concept:name'].unique()  # split data into test and training data
    train_ids, test_ids = train_test_split(case_ids, test_size=0.1, random_state=42)
    train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
    test_log = event_log[event_log['case:concept:name'].isin(test_ids)]
    return train_log, test_log


if __name__ == "__main__":

    file_path = "Testing/receipt.xes"

    try:
        event_log = pm4py.read_xes(file_path)
    except Exception as e:
        print(f"Error reading XES file: {e}")
        exit(1)

    # Process tree
    generate_process_tree(event_log)

    # Petri net
    generate_petri_netz(event_log)

    # Dotted chart
    generate_dotted_chart(event_log)

    # split data and discover petri net
    train_log, test_log = split_data(event_log)
    pn, im, fm = pm4py.discover_petri_net_inductive(event_log)
    pm4py.view_petri_net(pn, im, fm)

    # Fitness token-based replay
    pm4py.fitness_token_based_replay(test_log, pn, im, fm)

    # Conformance checking: Alignments
    pm4py.conformance_diagnostics_alignments(test_log, pn, im, fm)