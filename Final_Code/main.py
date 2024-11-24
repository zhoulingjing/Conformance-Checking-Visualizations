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
from tkinter import ttk
from tkinter import filedialog
import performance_spectrum
from tkinter import messagebox


file_path = None
root = tk.Tk()
root.title ("Implementation of Process Mining Visualizations for Conformance Checking")
root.geometry ("600x300")
start_screen =tk.Frame(root, bg="lavender")
vis_screen = tk.Frame(root, bg ="white")

def go_to_start_screen():
    vis_screen.pack_forget()
    start_screen.pack(fill="both", expand =True)

def go_to_vis_screen():
    start_screen.pack_forget()
    vis_screen.pack(fill="both", expand =True)





start_message = tk.Label(
    start_screen,
    text="Process Mining Visualizer",
    font=("Helvetica", 22),
    bg = "lavender")
start_message.pack (pady =50)

def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All Files", "*.*"), ("CSV Files", "*.csv"), ("XES Files", "*.csv")]
    )
    if file_path:
     go_to_vis_screen()

button_upload_file_next_screen = tk.Button(
    start_screen,
    text="Upload file",
    command=upload_file)

button_upload_file_next_screen.pack()


style = ttk.Style()
style.configure (
    "Custom.TCombobox",
    foreground="blue violet",
    background="white",
    fieldbackground="pink",
    font=("Helvetica", 14)  # Font and size
)

dropdown_var = tk.StringVar(value="Choose")
dropdown = ttk.Combobox(vis_screen, textvariable=dropdown_var, state="readonly", style="Custom.TCombobox"  )
dropdown['values'] = ['Petri Nets', 'Dotted Chart', 'Performance Spectrum', 'Process Tree', 'Activity Interaction Network', 'Conformance Heatmap', 'Semantic Conformance Word Cloud']
dropdown.pack(pady=40)


def generate_visualization():
    buttonname = dropdown_var.get()
    if (buttonname=="Petri Nets"):
        dottedpetri.generate_petri_net(file_path)
    elif (buttonname ==  "Dotted Chart"):
        dottedpetri.generate_dotted_chart(file_path)
    elif (buttonname ==  "Performance Spectrum"):
       performance_spectrum.generate_performance_spectrum(file_path)
    elif (buttonname ==  "Process Tree"):
       dottedpetri.generate_process_tree(file_path)
    elif (buttonname =="Activity Interaction Network"):
        messagebox.showwarning("Warning", "This visualization isn't implemented yet")
    elif (buttonname == "Conformance Heatmap"):
        messagebox.showwarning("Warning", "This visualization isn't implemented yet")
    elif (buttonname== "Semantic Conformance Word Cloud"):
        messagebox.showwarning("Warning", "This visualization isn't implemented yet")




    print (buttonname)


button_visualize = tk.Button (vis_screen,
                              text = "Generate Visualization",
                              command = generate_visualization,
                              bg="lightpink",
                              font = ("Helvetica", 10))
button_visualize.pack(pady = 20)

button_go_to_start = tk.Button(vis_screen,
                               text="Go to Start Screen",
                               command=go_to_start_screen,
                               bg = "lavender",
                               font = ("Helvetica", 10))
button_go_to_start.pack(pady=30)


start_screen.pack(fill="both", expand = True)
root.mainloop()