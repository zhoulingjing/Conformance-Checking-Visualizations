import pm4py
import numpy as np
import matplotlib as mlib
import pandas as pd
import sequence_emb_conf
import Project_code.semantic_conformance_word as semantic_conformance_word
import import_t
import conformance_heatmap_vis
import activity_interaction_network
import tkinter as tk
import dotted_chart_petri_bpmn as dottedpetri


from tkinter import ttk


file_path = r"C:\AAA\RWTH\Sem 7\SPP\Conformance-Checking-Visualizations\Project_code\receipt.csv"

root = tk.Tk()
root.title ("Implementation of Process Mining Visualizations for Conformance Checking")
root.geometry ("1000x600")
start_screen =tk.Frame(root, bg="pink")
vis_screen = tk.Frame(root)

def on_button_click(button_name):
    if (button_name == "Petri Nets"):
        dottedpetri.generate_petri_netz(import_t.import_csv(file_path))

    if (button_name == "Dotted Chart"):
        dottedpetri.generate_dotted_chart(import_t.import_csv(file_path))
        
    if (button_name == "Performance Spectrum"):
        dottedpetri.generate_dotted_chart(import_t.import_csv(file_path))

        

    print(f"{button_name} clicked")

def go_to_start_screen():
    vis_screen.pack_forget()
    start_screen.pack(fill="both", expand =True)

def go_to_vis_screen():
    start_screen.pack_forget()
    vis_screen.pack(fill="both", expand =True)





#Start screen
#start_screen =tk.Frame(root)
#start_screen.pack(fill="both", expand = True)
start_message = tk.Label(start_screen, text="Welcome to Our Project!", font=("Helvetica", 22), bg = "Pink")
start_message.pack (pady =50)

button_upload_file_next_screen = tk.Button(start_screen, text="Upload file", command=go_to_vis_screen)
button_upload_file_next_screen.pack()

#Screen with visualizations
#vis_screen = tk.Frame(root)


right_frame = tk.Frame(vis_screen, width=400, height=600)
right_frame.pack(side="right", fill="both", expand=False)
right_frame.pack_propagate(False)

dropdown_var = tk.StringVar(value="Choose")
dropdown = ttk.Combobox(right_frame, textvariable=dropdown_var, state="readonly")
dropdown['values'] = ['Petri Nets', 'Dotted Chart', 'Process Tree', 'Activity Interaction Network', 'Conformance Heatmap', 'Semantic Conformance Word Cloud']
dropdown.pack(pady=20)

button_go_to_start = tk.Button(vis_screen, text="Go to Start Screen", command=go_to_start_screen)
button_go_to_start.pack(side="bottom", anchor="se", padx=10, pady=10)

def generate_visualization():
    buttonname = dropdown_var.get()
    if (buttonname=="Petri Nets"):
        dottedpetri.generate_petri_netz(import_t.import_csv(file_path))
    elif (buttonname ==  "Dotted Chart"):
        dottedpetri.generate_dotted_chart(import_t.import_csv(file_path))
    elif (buttonname ==  "Performance Spectrum"):
        dottedpetri.generate_dotted_chart(import_t.import_csv(file_path))


    print (buttonname)


button_visualize = tk.Button (vis_screen, text = "Generate Visualization", command = generate_visualization)
button_visualize.pack(side = "bottom", anchor ="e", padx = 10, pady = 10)





start_screen.pack(fill="both", expand = True)
root.mainloop()