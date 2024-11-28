import pm4py
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns

if __name__ == "__main__":
    # import the log file
    file_path = './receipt.csv'
    
    event_log = pd.read_csv(file_path)
    event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name', activity_key='concept:name',
                                           timestamp_key='time:timestamp')
    
    # split the data for training
    case_ids = event_log['case:concept:name'].unique()
    train_ids, test_ids = train_test_split(case_ids, test_size=0.5, random_state=42)
    train_log = event_log[event_log['case:concept:name'].isin(train_ids)]
    test_log = event_log[event_log['case:concept:name'].isin(test_ids)]

    # train model
    model, im, fm = pm4py.discover_petri_net_inductive(train_log)
    # make a ditionary of trace and time and fitness
    data = []
    for id in test_log['case:concept:name'].unique():
        log = test_log[test_log['case:concept:name'] == id]
        diagnostics = pm4py.conformance_diagnostics_token_based_replay(log, model, im, fm)
        conformance = diagnostics[0]

        data.append({
            'trace_id': id,
            'trace_time': pd.to_datetime(log['time:timestamp']).min(),
            'fitness': conformance['trace_fitness']
        })

    df = pd.DataFrame(data)
    
    # convert timestamps to dates
    df['date'] = df['trace_time'].dt.date

    # assign the axis
    heatmap_data = df.pivot(index='trace_id', columns='date', values='fitness')

    # plot the heatmap using plt
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=False, cbar=True, vmin=0.97, vmax=1.0)
    plt.title('Conformance Heatmap with Concept Drift Over Time')
    plt.xlabel('Date')
    plt.ylabel('Trace IDs')
    plt.show()