"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

taylortextacular_app.py: main file for loading the files as well as loading the visualizations specified by specific
user-defined functions from the visualization library (taylorviz)
"""

# import necessary libraries
from nlp import Nlp
from exception import LoadStopWordError
import nltk
import taylorviz as tviz


def main():
    # download a package needed for sentiment analysis
    nltk.download('vader_lexicon')

    # download a package needed for removing the stop words from a file
    nltk.download('stopwords')

    # initialize framework
    ts = Nlp()

    # create a list of the files getting registered, a list of their labels, a list of the visualization functions
    # used to illustrate word data about them, and a list of labels for the visualizations
    files = ['TaylorSwiftOurSong.txt', 'TaylorSwiftFearless.txt', 'TaylorSwiftDearJohn.txt', 'TaylorSwiftRed.txt',
             'TaylorSwiftWelcometoNewYork.txt', 'TaylorSwiftGetawayCar.txt', 'TaylorSwiftLover.txt',
             'TaylorSwiftCardigan.txt', 'TaylorSwiftWillow.txt', 'TaylorSwiftLavenderHaze.txt']
    file_labels = ['Our Song', 'Fearless', 'Dear John', 'Red', 'Welcome to New York', 'Getaway Car', 'Lover',
                   'Cardigan', 'Willow', 'Lavender Haze']
    vis_funcs = [tviz.wordcount_sankey, tviz.sentiment_scatter, tviz.avgwlength_boxplot, tviz.avgwlength_bar,
                 tviz.total_wordl_boxplot]
    vis_names = ['wordcountsankey', 'sentimentscatter', 'avgwlengthboxplot', 'avgwlengthbar', 'totalwordlengthboxplot']

    # colors used for the word cloud
    word_cloud_colors = ['summer', 'Wistia', 'BuPu', 'Reds', 'Blues', 'bone', 'spring_r', 'gist_yarg', 'copper',
                         'Purples']

    try:
        # register some text files
        for i in range(len(files)):
            ts.load_text(files[i], file_labels[i])

    except LoadStopWordError as pe:
        # indicates whether there was an issue with registering the files
        print(str(pe))

    # load all the visualization functions that don't require parameters
    for i in range(len(vis_funcs)):
        ts.load_visualization(name=vis_names[i], vizfunc=vis_funcs[i])

    # produces a word cloud that visualizes the distinct word counts from each file
    ts.load_visualization('wordcloud', tviz.make_word_clouds, colormaps=word_cloud_colors)

    # makes sentiment analysis bar subplots (positive vs. neutral vs. negative scores) for each of the files passed in
    ts.load_visualization('sentimentbar', tviz.sentiment_analysis_bars, 5, 2)

    # display all the loaded visualizations
    ts.visualize()


if __name__ == '__main__':
    main()
