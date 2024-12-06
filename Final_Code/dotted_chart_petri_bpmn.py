import os
import pm4py
from pm4py.algo.conformance.tokenreplay import algorithm
from sklearn.model_selection import train_test_split


# Generate and save a dotted chart
def generate_dotted_chart(event_log, output_dir):
    try:
        output_path = os.path.join(output_dir, "dotted_chart.png")
        pm4py.save_vis_dotted_chart(event_log, output_path)
        print(f"Dotted chart saved to {output_path}.")
    except Exception as e:
        print("Failed to generate the dotted chart:", e)


# Generate and save a Petri net
def generate_petri_net(event_log, output_dir):
    try:
        net, im, fm = pm4py.discover_petri_net_inductive(event_log, activity_key='concept:name',
                                                         case_id_key='case:concept:name',
                                                         timestamp_key='time:timestamp')
        output_path = os.path.join(output_dir, "petri_net.png")
        pm4py.save_vis_petri_net(net, im, fm, output_path)
        print(f"Petri net saved to {output_path}.")
    except Exception as e:
        print("Failed to generate the Petri net chart:", e)


# Generate and save a BPMN model
def generate_bpmn(event_log, output_dir):
    try:
        process_tree = pm4py.discover_process_tree_inductive(event_log)
        bpmn_model = pm4py.convert_to_bpmn(process_tree)
        output_path = os.path.join(output_dir, "bpmn_model.png")
        pm4py.save_vis_bpmn(bpmn_model, output_path)
        print(f"BPMN model saved to {output_path}.")
    except Exception as e:
        print("Failed to generate the BPMN chart:", e)


# Split the data into train and test logs
def split_data(event_log):
    try:
        case_ids = event_log['case:concept:name'].unique()
        train_ids, test_ids = train_test_split(case_ids, test_size=0.1, random_state=42)
        train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
        test_log = event_log[event_log['case:concept:name'].isin(test_ids)]
        print("Data split into training and test logs.")
        return train_log, test_log
    except Exception as e:
        print("Failed to split the data:", e)

