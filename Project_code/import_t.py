import pandas as pd
import pm4py


def import_csv(file_path):
    try:
        event_log = pd.read_csv(file_path)

        print("Columns in CSV:", event_log.columns)

        event_log['time:timestamp'] = pd.to_datetime(event_log['time:timestamp'])

        event_log = pm4py.format_dataframe(
            event_log,
            case_id='case:concept:name',     
            activity_key='concept:name',      
            timestamp_key='time:timestamp'    
        )

        print(event_log.head())

        start_activities = pm4py.get_start_activities(event_log)
        end_activities = pm4py.get_end_activities(event_log)

        print("Start activities:", start_activities)
        print("End activities:", end_activities)

        return event_log
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    file_path = "Project_code/receipt.csv"
    event_log = import_csv(file_path)
