from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pm4py
from sklearn.model_selection import train_test_split


def get_unique_variants(event_log):
    traces = []
    vars = pm4py.get_variants(event_log)
    for trace in vars:
        traces.append(trace)
    return traces


def calc_frequency(activities):
    frequencies = {}
    for activity in activities:
        if activity in frequencies:
            frequencies[activity] += 1
        else:
            frequencies[activity] = 1
    return frequencies


def find_sig_trace(event_log):
    traces = get_unique_variants(event_log)
    # model, im, fm = pm4py.discover_petri_net_inductive(event_log) 
    trace_list = []
    for trace in traces:
            subset_trace = []
            trace_length=0
            for activity in trace:
                subset_trace.append(activity)
            trace_length=len(subset_trace)
            trace_list.append({
                "trace": trace,  # List of activities in the trace
                "length": trace_length  # Length of the trace
            })
    longest_trace_dict = max(trace_list, key=lambda trace_dict: trace_dict["length"])
    return longest_trace_dict["trace"]


def get_conformance_score(word, trace):
    return trace.count(word)


def color_by_conformance(word, trace):
    conformance_score = get_conformance_score(word, trace)
    if conformance_score > 1:
        return 'blue'
    elif conformance_score == 1:
        return 'green'
    else:
        return 'red'


def make_word_cloud(file_path):
    # Load the event log
    event_log = pm4py.read_xes(file_path)
    significant_trace = find_sig_trace(event_log)
    
    # Load the CSV and process the text
    df = pm4py.convert.convert_to_dataframe(event_log)
    txt = ",".join(df['concept:name'].astype(str))
    phrases = txt.split(",")

    # Count the frequency of each phrase
    phrase_counts = calc_frequency(phrases)

    # Generate the word cloud
    def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return color_by_conformance(word, significant_trace)

    wc = WordCloud(
        background_color="white",
        colormap="viridis",
        width=800,
        height=400,
        color_func=custom_color_func
    )
    word_cloud = wc.generate_from_frequencies(phrase_counts)

    # Display the word cloud
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig('../images/scw.png') 
    plt.show()



# Example usage
make_word_cloud(r'./running-example.xes')
