from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pm4py
import matplotlib.colors as mcolors
import numpy as np
import os 
import pandas

def get_unique_variants(event_log):
    """Extract unique trace variants from the event log."""
    return list(pm4py.get_variants(event_log).keys())

def calc_frequency(activities):
    """Calculate frequency of activities in the log."""
    frequencies = {}
    for activity in activities:
        frequencies[activity] = frequencies.get(activity, 0) + 1
    return frequencies

def find_sig_trace(event_log):
    """Find the longest trace in the event log."""
    traces = get_unique_variants(event_log)
    return max(traces, key=len)

def get_conformance_score(word, trace):
    """Calculate the conformance score of a word in a trace."""
    return trace.count(word)

def color_by_conformance(word, trace, max_score):
    """Return a color for a word based on its conformance score."""
    conformance_score = get_conformance_score(word, trace)
    normalized_score = conformance_score / max_score
    colormap = mcolors.LinearSegmentedColormap.from_list("conformance", ["red", "yellow", "green", "blue"])
    return mcolors.rgb2hex(colormap(normalized_score))


def convert_to_dataframe(file_path):
    type = os.path.splitext(file_path)
    if type[1] == '.xes':
        event_log = pm4py.read_xes(file_path)


    elif type[1] == '.csv':
        event_log = pandas.read_csv(file_path)
        event_log = pm4py.format_dataframe(event_log, case_id='case:concept:name',activity_key='concept:name',timestamp_key='time:timestamp')

    return event_log


def make_word_cloud(file_path):
    # Load the event log
    event_log = convert_to_dataframe(file_path)
    significant_trace = find_sig_trace(event_log)

    # Process the log to extract activity names
    df = pm4py.convert.convert_to_dataframe(event_log)
    activities = df['concept:name'].astype(str)
    phrase_counts = calc_frequency(activities)

    # Get maximum conformance score
    max_conformance_score = max([get_conformance_score(word, significant_trace) for word in phrase_counts])

    # Custom color function for WordCloud
    def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return color_by_conformance(word, significant_trace, max_conformance_score)

    # Generate the word cloud
    wc = WordCloud(
        background_color="white",
        width=800,
        height=400,
        color_func=custom_color_func
    )
    word_cloud = wc.generate_from_frequencies(phrase_counts)

    # Plot word cloud and thin color bar
    fig, ax = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [5, 0.2]})

    # Word cloud
    ax[0].imshow(word_cloud, interpolation="bilinear")
    ax[0].axis("off")
    ax[0].set_title("Word Cloud with Conformance Scores", fontsize=14, fontweight='bold')

    # Color bar logic
    colormap = mcolors.LinearSegmentedColormap.from_list("conformance", ["red", "yellow", "green", "blue"])
    norm = mcolors.Normalize(vmin=0, vmax=max_conformance_score)
    gradient = np.linspace(0, 1, 256).reshape(-1, 1)

    # Display the thin color bar
    ax[1].imshow(gradient, aspect="auto", cmap=colormap)
    ax[1].axis("off")

    # Add clear Low and High Conformance labels
    fig.text(0.91, 0.12, "High Conformance", fontsize=5, color="blue", ha="center", va="center")
    fig.text(0.91, 0.88, "Low Conformance", fontsize=5, color="red", ha="center", va="center")

    # Adjust layout
    plt.subplots_adjust(wspace=0.1, right=0.9)
    plt.tight_layout()
    plt.savefig('./Final_Code/output_images/semantic_conformance_word_cloud.png')
    plt.show()

# Example usage
#make_word_cloud('Final_Code/running-example.xes')
