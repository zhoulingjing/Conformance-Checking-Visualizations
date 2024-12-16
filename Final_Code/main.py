import pm4py
import numpy as np
import matplotlib as mlib
import pandas as pd
import sequence_emb_conf
import senantic_conformance_word
import import_t
import conformance_heatmap_vis
import activity_interaction_network
<<<<<<< Updated upstream
import tkinter as tk
import dotted_chart_petri_bpmn as dottedpetri
from tkinter import ttk
from tkinter import filedialog
import performance_spectrum
from tkinter import messagebox

=======
import senantic_conformance_word
import pandas as pd
>>>>>>> Stashed changes

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


<<<<<<< Updated upstream
=======

def upload_file():
    """Handle file upload and show preview."""
    global file_path, event_log
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("CSV or XES Files", "*.csv *.xes"), ("All Files", "*.*")]
    )
    
    if file_path:
        try:
            # Show file preview before visualization
            if file_path.endswith('.csv'):
                # For CSV files, load the first few rows using pandas
                df = pd.read_csv(file_path)
                preview_text = df.head().to_string(index=False)  # Show the first 5 rows (as a string without index)
            elif file_path.endswith('.xes'):
                # For XES files, show a preview (you could choose to display the first few traces)
                event_log = pm4py.read_xes(file_path)
                preview_text = str(event_log[:5])  # Just a simple preview of the first 5 events
            else:
                preview_text = "Unsupported file type"

            # Create a new window for the preview
            preview_window = tk.Toplevel(root)
            preview_window.title("File Preview")
            preview_window.geometry("600x300")

            # Label to show the file preview
            preview_label = tk.Label(preview_window, text="File Preview (first few lines):", font=("Helvetica", 12))
            preview_label.pack(pady=10)

            preview_content = tk.Label(preview_window, text=preview_text, font=("Courier", 10), justify="left")
            preview_content.pack(pady=10)

            # Add a confirm button to proceed to the visualization screen
            def confirm_file():
                try:
                    event_log = convert_to_event_log(file_path)
                    go_to_vis_screen()
                    preview_window.destroy()  # Close preview window
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process the file: {e}")
                    preview_window.destroy()

            confirm_button = tk.Button(preview_window, text="Confirm and Proceed to Visualization", command=confirm_file)
            confirm_button.pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview the file: {e}")

>>>>>>> Stashed changes



<<<<<<< Updated upstream
=======

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
        elif buttonname == "Word Cloud":  
            senantic_conformance_word.make_word_cloud(file_path)  
        else:
            messagebox.showwarning("Warning", "Invalid option selected.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate visualization: {e}")


# Start screen
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
dropdown = ttk.Combobox(vis_screen, textvariable=dropdown_var, state="readonly", style="Custom.TCombobox"  )
dropdown['values'] = ['Petri Nets', 'Dotted Chart', 'Performance Spectrum', 'Process Tree', 'Activity Interaction Network', 'Conformance Heatmap', 'Semantic Conformance Word Cloud']
=======
dropdown = ttk.Combobox(vis_screen, textvariable=dropdown_var, state="readonly", style="Custom.TCombobox")
dropdown['values'] = ['Petri Nets', 'Dotted Chart', 'Performance Spectrum', 'bpmn', 'Activity Interaction Network',
                      'Conformance Heatmap with Concept Drift', 'Temporal Behavior Patterns Chart','Word Cloud']
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream

start_screen.pack(fill="both", expand = True)
root.mainloop()
=======
start_screen.pack(fill="both", expand=True)
root.mainloop()


>>>>>>> Stashed changes
