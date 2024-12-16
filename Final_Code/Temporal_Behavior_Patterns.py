import pm4py
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import cm
import colorsys
import os

#calculate frecuency of each activity
def calc_frequency(event_log):
    frequencies = {}
    for activity in event_log['concept:name']:
        if activity in frequencies.keys():
            frequencies[activity] += 1
        else:
            frequencies.update({activity: 1})
    return frequencies

#get all unique activities
def get_unique_activities(event_log):
    return list(set(event_log['concept:name']))

#get unique timestamps
def get_unique_time(time):
    times = []
    for i in time:
        if i in times:
            continue
        else:
            times.append(i)
    return times

#sort time in chronological order
def sort_time(event_log, time_format):
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
            return sorted(event_log['time:timestamp'], key=days.get)

        case 'hours':
            return sorted(event_log['time:timestamp'], key=lambda x: datetime.strptime(x, "%H:%M").time())

        case 'years':
            return sorted(event_log['time:timestamp'], key=int)

#change timestamp based on the given time_format
def process_timestamp(event_log, time_format):
    event_log['time:timestamp'] = pd.to_datetime(event_log['time:timestamp'])
    match time_format:
        case 'hours':
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.round('60min')
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.strftime("%H:00")
# 14:58 14pm
        case 'days':
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.strftime("%A")

        case 'months':
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.strftime("%b")

        case 'years':
            event_log['time:timestamp'] = event_log['time:timestamp'].dt.strftime("%Y")
    return event_log

#for a given target_time give frequency of all activities that happen at that time
def match_activity(event_log, target_time):
    matched_activities = event_log[event_log['time:timestamp'] == target_time]
    frequencies = calc_frequency(matched_activities)
    return frequencies

#generate colors for different activities
def generate_color(index, total):
    hue = index / total  # Evenly spaced hues
    saturation = 0.8     # High saturation for vibrant colors
    value = 0.9          # High brightness
    return colorsys.hsv_to_rgb(hue, saturation, value)

#convert csv and xes to dataframe
def convert_to_dataframe(file_path):
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)


    elif type[1] == '.csv':
        event_log = pd.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name',activity_key='concept:name',timestamp_key='time:timestamp')

    return event_log


def generate_Temporal_Behavior_Chart(file_path, time_format):
    
    event_log = convert_to_dataframe(file_path)
    event_log = process_timestamp(event_log, time_format)

    figure, axs = plt.subplots(figsize=(12, 6))

    unique_activities = get_unique_activities(event_log)
    color_map = {activity: generate_color(i, len(unique_activities)) for i, activity in enumerate(unique_activities)}

    sorted_time = sort_time(event_log, time_format)
    unique_time = get_unique_time(sorted_time)
    plotted_activities = []

    # Collect frequency data for dotted lines
    activity_frequency_over_time = {activity: [] for activity in unique_activities}

    for time in unique_time:
        activities = match_activity(event_log, time)
        x = [time]
        for activity in unique_activities:
            frequency = activities.get(activity, 0)
            activity_frequency_over_time[activity].append(frequency)
            y = frequency 
            if activity not in plotted_activities:
                plt.plot(x, y, 'o', color=color_map[activity], label=activity)
                plotted_activities.append(activity)
            else:
                plt.plot(x, y, 'o', color=color_map[activity])

    # Add dotted lines for each activity
    for activity, frequencies in activity_frequency_over_time.items():
        x_positions = range(len(unique_time))  # Map unique times to sequential indices
        plt.plot(x_positions, frequencies, '--', color=color_map[activity], alpha=0.7)

    # Configure the plot
    plt.xticks(ticks=range(len(unique_time)), labels=unique_time, rotation=45)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Activities")
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('./Final_code/output_images/tbp.png', dpi=900)
    plt.show()
