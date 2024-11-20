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
import dotted_chart_petri_bpmn as dottedpetri


file_path = r"E:\Conformance-Checking-Visualizations\Project_code\receipt.csv"

root = tk.Tk()
root.title ("Implementation of Process Mining Visualizations for Conformance Checking")
root.geometry ("1000x600")

def on_button_click(button_name):
    if (button_name == "Petri Nets"):
        dottedpetri.generate_petri_netz(import_t.import_csv(file_path))

    if (button_name == "Dotted Chart"):
        dottedpetri.generate_dotted_chart(import_t.import_csv(file_path))
        
    if (button_name == "Performance Spectrum"):
        dottedpetri.generate_dotted_chart(import_t.import_csv(file_path))

        

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