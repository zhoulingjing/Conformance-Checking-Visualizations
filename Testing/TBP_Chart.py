import pandas
import pm4py
import matplotlib.pyplot as plt
import math

def calc_frequency(event_log):
    frequencies = {}
    for activity in event_log['Activity']:
        if activity in frequencies.keys():
            frequencies[activity] += 1
        else:
            frequencies.update({activity : 1})
    return frequencies

def TBP_Chart(event_log, date_type = 'hours'):
    time = []
    x_labels = []

    if date_type == 'hours':
        x_labels = [f"{i}:00" for i in range(24)]
    elif date_type == 'days':
        x_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    elif date_type == 'months':
        x_labels =['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    else:
        raise ValueError("x_type must be 'hours','days' or 'months'")

    frequencies = calc_frequency(event_log)
    fig, axes = plt.subplots()
    plt.xticks(range(len(x_labels)),x_labels)
    plt.yticks(range(len(frequencies)+2))
    plt.show()


x = pandas.read_csv("running-example.csv")
TBP_Chart(x,date_type='months')