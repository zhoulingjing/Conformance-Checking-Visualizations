import pm4py
import pandas
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import dotted_chart_petri_bpmn as dottedpetri
import performance_spectrum
import conformance_heatmap_vis
import Temporal_Behavior_Patterns

import activity_interaction_network
import senantic_conformance_word

file_path = None
event_log = None


root = tk.Tk()
root.title("Implementation of Process Mining Visualizations for Conformance Checking")
root.geometry("600x300")
start_screen = tk.Frame(root, bg="lavender")
vis_screen = tk.Frame(root, bg="white")

output_dir = './Final_Code/output_images'
os.makedirs(output_dir, exist_ok=True)

def go_to_start_screen():
    """Switch to the start screen."""
    vis_screen.pack_forget()
    start_screen.pack(fill="both", expand=True)


def go_to_vis_screen():
    """Switch to the visualization screen."""
    start_screen.pack_forget()
    vis_screen.pack(fill="both", expand=True)


def upload_file():
    """Handle file upload and proceed to visualization screen."""
    global file_path, event_log
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("CSV or XES Files", "*.csv *.xes"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            event_log = convert_to_event_log(file_path)
            go_to_vis_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the file: {e}")


def convert_to_event_log(file_path):
    """Convert the uploaded file into an event log."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.xes':
        return pm4py.read_xes(file_path)
    elif ext == '.csv':
        df = pandas.read_csv(file_path)
        return pm4py.format_dataframe(df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def generate_visualization():
    """Generate the selected visualization."""
    global file_path

    if file_path is None:
        messagebox.showerror("Error", "Please upload a file first!")
        return

    # Load the event log
    event_log = convert_to_event_log(file_path)
    if event_log is None or event_log.empty:
        messagebox.showerror("Error", "The uploaded file could not be processed or is empty.")
        return

    buttonname = dropdown_var.get()
    try:
        if buttonname == "Petri Nets":
            dottedpetri.generate_petri_net(event_log,output_dir)
        elif buttonname == "Dotted Chart":
            dottedpetri.generate_dotted_chart(event_log,output_dir)
        elif buttonname == "Performance Spectrum":
            performance_spectrum.generate_performance_spectrum(file_path,output_dir)
        elif buttonname == "bpmn":
            dottedpetri.generate_bpmn(event_log, output_dir)
        elif buttonname == "Activity Interaction Network":
            activity_interaction_network.generate_activity_interaction_network_with_edge_fitness(file_path)
        elif buttonname == "Semantic Conformance Word Clouds":
            senantic_conformance_word.make_word_cloud(file_path)
        elif buttonname == "Conformance Heatmap with Concept Drift":
          if file_path and file_path.endswith(".csv"):
            messagebox.showwarning(
            "Warning",
            "For more detailed graphs, please use .xes files instead of .csv files.",
            parent=root
        )
            conformance_heatmap_vis.generate_conformance_heatmap_with_time(file_path)
          else:
            conformance_heatmap_vis.generate_conformance_heatmap_with_time(file_path)
        elif buttonname == "Temporal Behavior Patterns Chart":
            Temporal_Behavior_Patterns.generate_Temporal_Behavior_Chart(file_path , "days")
        else:
            messagebox.showwarning("Warning", "Invalid option selected.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate visualization: {e}")


# Start screen
start_message = tk.Label(
    start_screen,
    text="Process Mining Visualizer",
    font=("Helvetica", 22),
    bg="lavender"
)
start_message.pack(pady=50)

button_upload_file_next_screen = tk.Button(
    start_screen,
    text="Upload File",
    command=upload_file
)
button_upload_file_next_screen.pack()

# Visualization screen
style = ttk.Style()
style.configure(
    "Custom.TCombobox",
    foreground="blue violet",
    background="white",
    fieldbackground="pink",
    font=("Helvetica", 14)
)

dropdown_var = tk.StringVar(value="Choose")
dropdown = ttk.Combobox(vis_screen, textvariable=dropdown_var, state="readonly", style="Custom.TCombobox", width=40)
dropdown['values'] = ['Petri Nets', 'Dotted Chart', 'Performance Spectrum', 'bpmn', 'Activity Interaction Network',
                      'Conformance Heatmap with Concept Drift', 'Temporal Behavior Patterns Chart', 'Semantic Conformance Word Clouds']
dropdown.pack(pady=40)

button_visualize = tk.Button(
    vis_screen,
    text="Generate Visualization",
    command=generate_visualization,
    bg="lightpink",
    font=("Helvetica", 10)
)
button_visualize.pack(pady=20)

button_go_to_start = tk.Button(
    vis_screen,
    text="Go to Start Screen",
    command=go_to_start_screen,
    bg="lavender",
    font=("Helvetica", 10)
)
button_go_to_start.pack(pady=30)

start_screen.pack(fill="both", expand=True)
root.mainloop()