import pm4py
import pandas
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
from matplotlib.pyplot import cm
import numpy as np 



def calc_frequency(event_log):
    frequencies = {}
    for activity in event_log['concept:name']:
        if activity in frequencies.keys():
            frequencies[activity] += 1
        else:
            frequencies.update({activity : 1})
    return frequencies



def get_unique_activities(event_log):
    return list(set(event_log['concept:name']))



def get_unique_time(time):
    return list(set(time))




def sort_time(event_log,time_format):
    match time_format:
        case 'months':
            months = {
                    'Jan': 0,
                    'Feb': 1,
                    'Mar': 2,
                    'Apr': 3,
                    'May': 4,
                    'Jun': 5,
                    'Jul': 6,
                    'Aug': 7,
                    'Sep': 8,
                    'Oct': 9,
                    'Nov': 10,
                    'Dec': 11,
                }
            return sorted(event_log['time:timestamp'], key=months.get)
        case 'days':
            days = {
                'Monday': 1,
                'Tuesday': 2,
                'Wednesday': 3,
                'Thursday': 4,
                'Friday': 5,
                'Saturday': 6,
                'Sunday': 7,
            }
            return sorted(event_log['time:timestamp'], key= days.get)

        case 'hours':
            return sorted(event_log['time:timestamp'], key=lambda x: datetime.strptime(x, "%H:%M").time())
        
        case 'years':
            return sorted(event_log['time:timestamp'], key=int)



def process_timestamp(event_log,time_format):
    event_log['time:timestamp'] = pandas.to_datetime(event_log['time:timestamp'])
    match time_format:
        case 'hours':  # Group by hours of a single day
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.strftime("%H:00")
            
        case 'days':  # Group by days of a single month
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.strftime("%A")

        case 'months':  # Group by months of a single year
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.strftime("%b")

        case 'years':  # Group by years (unchanged)
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.strftime("%Y")
    return event_log


def match_activity(event_log, target_time):
    matched_activities = event_log[event_log['time:timestamp'] == target_time]
    frecuencies = calc_frequency(matched_activities)
    return frecuencies



def Temporal_Behavior_Patterns(event_log, time_format):
    event_log = process_timestamp(event_log,time_format)
    figure, axs = plt.subplots(figsize=(12,6))

    unique_activities = get_unique_activities(event_log)
    colors = plt.cm.tab20.colors  # Use a colormap with distinct colors
    color_map = {activity: colors[i % len(colors)] for i, activity in enumerate(unique_activities)}

    sorted_time = sort_time(event_log,time_format)
    unique_time = get_unique_time(sorted_time)
    for time in unique_time:
        x = []
        y = []
        activities = match_activity(event_log,time)
        x = [time]
        for activity, frequency in activities.items():
            y.append(frequency)
            plt.plot(x,y,'o', color=color_map[activity],label=activity)
            y.remove(frequency)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Activities")
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()
        
event_log = pm4py.read_xes('Testing/running-example.xes')    
Temporal_Behavior_Patterns(event_log,time_format='hours')


