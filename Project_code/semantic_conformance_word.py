from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

def calc_frequency(activities):
    # Create an empty dictionary to store frequencies
    frequencies = {}
    
    # Iterate through each activity
    for activity in activities:
        if activity in frequencies:
            # Increment the count if the activity is already in the dictionary
            frequencies[activity] += 1
        else:
            # Initialize the count if the activity is not in the dictionary
            frequencies[activity] = 1
    
    return frequencies
def get_conformance_score(word):
    # For demonstration: Higher frequency means higher conformance
    return word.lower().count('request') 

def color_by_conformance(word, *args, **kwargs):
    conformance_score = get_conformance_score(word)  
    if conformance_score > 1:
        return 'blue'  
    elif conformance_score == 1:
        return 'green'  
    else:
        return 'red' 

def make_word_cloud(file_path):
    df = pd.read_csv(file_path)
    txt = ",".join(df['concept:name'].astype(str))
    wc = WordCloud().generate(text=txt)
    phrases = txt.split(",")
    
    # Count the frequency of each phrase
    phrase_counts = calc_frequency(phrases)
    
    # Generate the word cloud from frequencies
    wc = WordCloud(background_color="white", colormap="viridis", width=800, height=400,color_func=color_by_conformance)
    word_cloud = wc.generate_from_frequencies(phrase_counts)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()

make_word_cloud(r'./running-example.csv')