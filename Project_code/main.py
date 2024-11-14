import pm4py
import numpy as np
import matplotlib as mlib
import pandas as pd
import sequence_emb_conf
import senantic_conformance_word
import import_t
import conformance_heatmap_vis
import activity_interaction_network
import tkinter as tk


def petri_nets_visualization ():
    print ("It is a petri net")
    return None

def performance_spectrum_visualization ():
    print("It is a performance spectrum")
    return None

def dotted_chart_visualization():
    print("It is Dotted Chart")
    return None




root = tk.Tk()
root.title ("Implementation of Process Mining Visualizations for Conformance Checking")
root.geometry ("1000x600")

def on_button_click(button_name):
    if (button_name == "Petri Nets"):
        petri_nets_visualization()

    if (button_name == "Dotted Chart"):
        dotted_chart_visualization()

    if (button_name == "Performance Spectrum"):
        performance_spectrum_visualization()

    print(f"{button_name} clicked")


buttons = []
button_names = ["Upload data", "AIN", "Conformance Heatmap", "SEC",
                "Semantic Conformance Word Cloud", "Petri Nets", "Performance Spectrum", "Dotted Chart"]

for i, name in enumerate(button_names):
    button = tk.Button(root, text=name, width=30, height=2,
                       command=lambda name=name: on_button_click(name))
    buttons.append(button)
    button.grid(row=i//4, column=i%4, padx=10, pady=10)
root.mainloop()






