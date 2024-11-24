import numpy as np
import matplotlib.pyplot as plt
import pm4py
import pandas
import os

def load_log(file_path):
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)

    elif type[1] == '.csv':
        event_log = pandas.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name',activity_key='concept:name',timestamp_key='time:timestamp')

def get_time(event_log):
    time = []
    for i in event_log['time:timestamp']:
        time.append(i)
    time = pandas.to_datetime(time)
    return time


def connect_two_points(x,p1,p2, axs):  #connect p1 with p2
    y = [10,0]
    x1, x2 = x[p1], x[p2]
    y1, y2 = y[p1%2], y[p2%2]
    axs.plot([x1,x2],[y1,y2], color ='blue')

#Test data
time_data = [1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10] # start-end time

def performance_spectrum(time_data):
    fig = plt.figure()
    gs = fig.add_gridspec(3,hspace = 0)             #create number of segments
    axs = gs.subplots(sharex=True, sharey=True)     
    plt.yticks([])       
    axs[0].set(xlim= (0,30),ylim = (0,10))                           
    for i in range(3):
        axs[i].set_ylabel("test",rotation = 0)
        axs[i].yaxis.set_label_coords(-0.05, 0.4)

    for j in range(3):
        for i in range(0,len(time_data),2):
            connect_two_points(time_data,i,i+1,axs[j])
    plt.show()

performance_spectrum(time_data)