"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

taylorviz.py: different visualization functions to illustrate findings about registered texts
"""
# import necessary libraries
from collections import defaultdict
import matplotlib.pyplot as plt
import sankey as sk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
from wordcloud import WordCloud


def convert_file_to_string(word_count, max_words=None):
    """ Extracts words from a file that have a frequency of one of the top user-defined integer frequencies in each file
    and compiles them into one sting
    Args:
        word_count (dict): contains the words in a file (key) and their frequencies (value)
        max_words (int): optional number of words considered from each file for analysis, based on their frequencies
    Returns:
        words (list): list of words of interest
    """
    # create empty string
    words = ''

    # if max_words is given, restrict the analysis to consider only the max_words number of words in each file based on
    # their frequencies
    if max_words is not None:
        # making sure that the maximum word specification is inputted as an integer
        assert isinstance(max_words, int), 'The number of words considered from each file for analysis must be an ' \
                                           'integer'
        word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                            reverse=True)}
        word_count = dict(word_count.items()[:max_words])

    for word, count in word_count.items():
        # Extract each word in the word count dictionary and repeat them in the returned string based on their
        # frequency in the file
        word = (word + ' ') * count
        words += word

    # return the string
    return words


def wordcount_sankey(data, word_list=None, k=5):
    """ Maps each text to words on a Sankey diagram, where the thickness of the line is the word's frequency in the text
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
        word_list (list): optional list containing a set of words (str) to be shown on the diagram
        k (int): the union of the k most common words across each file
    Returns:
        None (just generates a Sankey diagram!)
    """
    # Ensuring the inputted parameters are of a valid type
    assert isinstance(data, defaultdict), 'The data extracted from this file must be stored in a dictionary'

    if k is not None:
        # Ensuring that k is an integer and not inputted with a word list
        assert isinstance(k, int), 'The number of words considered from each file for analysis must be an integer'
        assert word_list is None, 'You cannot specify a list of words to be shown on the diagram while also ' \
                                  'specifying how many words you want to consider across each file'

    # Initializing a list containing a set of words to be shown on the diagram if not specified
    if word_list is None:
        word_list = []
    else:
        # Ensuring that word_list is a list of strings and not inputted with a k value
        assert isinstance(word_list, list), 'Must input the words to be shown on the diagram as a list'
        assert all(isinstance(word, str) for word in word_list), 'Word list must only contain strings'
        assert k is None, 'You cannot specify a list of words to be shown on the diagram while also specifying how ' \
                          'many words you want to consider across each file'

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # initialize empty lists
    texts = []
    all_words = []
    all_counts = []

    for text, word_count in word_count_dict.items():
        # Sorts the word counts in descending order by counts
        word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                            reverse=True)}
        # get a list of only the keys (words from each file)
        words = list(word_count.keys())

        if k is not None:
            # get only the top k words from a file and add them to a list of words to be shown on the diagram
            word_list += [word for word in words[:k]]

    for text, word_count in word_count_dict.items():
        # Sorts the word count dictionary in descending order by counts
        word_count = {word: count for word, count in sorted(word_count.items(), key=lambda item: item[1],
                                                            reverse=True)}

        for word, count in word_count.items():
            if word in word_list:
                # extracts the word, its count in a file, and the name of its file of origin and adds them to lists if
                # the word is in word_list or part of the k most popular words across each file
                all_words.append(word)
                all_counts.append(count)
                texts += [text]

    # use all_words, all_counts, and texts to create a dataframe containing word count information about the texts
    word_count = list(zip(all_words, all_counts, texts))
    df_word_counts = pd.DataFrame(word_count, columns=['Word', 'Counts', 'Text'])

    # use the new dataframe to create a Sankey diagram
    sk.make_sankey(df_word_counts, 0, 'Text', 'Word', vals=df_word_counts['Counts'])


def make_word_clouds(data, colormaps=None, background_color='black', min_font_size=4, normalize_plurals=True,
                     collocations=False, subplot_rows=4, subplot_columns=3, max_words=None):
    """ Creates a word cloud that shows the words in a text, with words that appear more frequently appearing larger
        Args:
            data (dict): data extracted from the file as a dictionary attribute--> raw data
            colormaps (list of strings): List of color schemes for the words on the diagram
            background_color (string): the color of the word cloud's background
            min_font_size (int): The minimum font size used for the words
            normalize_plurals (boolean): A boolean value indicating whether the trailing 's' in words should be removed
            collocations (boolean): A boolean value indicating whether bigrams are considered
            subplot_rows (int): the number of rows in the sub-plot
            subplot_columns (int): the number of columns in the sub-plot
            max_words (int): The maximum number of words represented on the word cloud
        Returns:
            None (just generates word clouds)
        """
    # Assertion statements for the input parameters
    if colormaps is not None:
        assert isinstance(colormaps, list), 'The color schemes of the word cloud must be entered in a list'
        assert all(isinstance(colormap, str) for colormap in colormaps), 'The color maps for each word cloud must be ' \
                                                                         'entered as strings'
    assert isinstance(background_color, str), 'The background color of the word cloud must be entered as a string'
    assert isinstance(min_font_size, int), 'The minimum font size of the word cloud must be entered as an integer'
    assert isinstance(normalize_plurals, bool), 'You must indicate whether the plural form of a word should be ' \
                                                'considered the same as its singular form with "True" or "False"'
    assert isinstance(collocations, bool), 'You must indicate whether bigrams are considered with "True" or "False"'
    assert isinstance(subplot_rows, int), 'The number of rows for the subplot must be an integer'
    assert isinstance(subplot_columns, int), 'The number of columns for the subplot must be an integer'

    # initialize empty lists
    texts = []
    word_strings = []

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # grab the words from each file and compile them into one string per file
    for text, word_count in word_count_dict.items():
        words = convert_file_to_string(word_count, max_words=max_words)

        # store the names of the files and their word strings into lists
        texts.append(text)
        word_strings.append(words)

    # initializes the word cloud figure
    plt.figure()

    # defines the default colormaps based on the number of registered texts
    if colormaps is None:
        colormaps = ['viridis'] * len(texts)

    for i in range(len(texts)):
        # generate a word cloud subplot for each file
        plt.subplot(subplot_rows, subplot_columns, i + 1)
        wordcloud = WordCloud(background_color=background_color, colormap=colormaps[i], min_font_size=min_font_size,
                              normalize_plurals=normalize_plurals, collocations=collocations).generate(word_strings[i])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        # Each subplot is labeled based on the text they are representing
        plt.gca().title.set_text('Word Cloud For "' + texts[i] + '"')

    # Gives the plot an overarching title
    plt.suptitle('Overall Word Counts')

    # resizes the graph to ensure that it can be clearly read
    plt.gcf().set_size_inches(50, 14)

    # adjusts spacing between graphs
    plt.subplots_adjust(wspace=.8, hspace=.8)

    # presents the word clouds
    plt.show()


def sentiment_scatter(data, max_words=None):
    """ Scatter plot with x being the positive score of a file and y being the file's negative score
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
        max_words (int): optional number of words considered from each file for analysis, based on their frequencies
    Returns:
        None (just generates a scatter plot)
    """
    # Ensuring the data types of the inputted parameters are valid
    assert isinstance(data, defaultdict), 'The data extracted from this file must be stored in a dictionary'

    # if max_words is given, restrict the analysis to consider only the max_words number of words in each file
    if max_words is not None:
        # making sure that the maximum word specification is inputted as an integer
        assert isinstance(max_words, int), 'The number of words considered from each file for analysis must be an ' \
                                           'integer'

    # initialize empty lists
    texts = []
    positive_distributions = []
    negative_distributions = []

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # initialize a sentiment intensity analyzer
    sia = SentimentIntensityAnalyzer()

    # grab the words from each file and compile them into one string per file
    for text, word_count in word_count_dict.items():
        words = convert_file_to_string(word_count, max_words=max_words)

        # calculate the sentiment scores (negative vs. neutral vs. positive) for each file and store them in a
        # dictionary
        sentiment_distribution = sia.polarity_scores(words)
        pos_score = sentiment_distribution['pos']
        neg_score = sentiment_distribution['neg']

        # store the names of the files as well as their sentiment distribution dictionaries
        texts.append(text)
        positive_distributions.append(pos_score)
        negative_distributions.append(neg_score)

    # plot the relationship between the positive score and negative score of a file
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.scatter(positive_distributions, negative_distributions)

    # Adds labels to each point on the scatter plot
    for i, txt in enumerate(texts):
        ax.annotate(txt, (positive_distributions[i], negative_distributions[i]))

    # calculate equation for trend line
    z = np.polyfit(positive_distributions, negative_distributions, 1)
    p = np.poly1d(z)

    # add trend line to plot
    plt.plot(positive_distributions, p(positive_distributions))

    # Adds labels to the scatter plot
    plt.xlabel('Positive Score')
    plt.ylabel('Negative Score')
    plt.title('Negative vs. Positive Score of Different Songs')
    plt.show()


def sentiment_analysis_bars(data, subplot_rows=5, subplot_columns=2, max_words=None):
    """ Creates a bar chart for each file representing their overall sentiments
    # Citation: https://realpython.com/python-nltk-sentiment-analysis/
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
        subplot_rows (int): optional number of rows in the sub-plot
        subplot_columns (int): optional number of columns in the sub-plot
        max_words (int): optional number of words considered from each file for analysis, based on their frequencies
    Returns:
        None (just generates bar charts!)
    """
    # Checking whether the types of the inputted parameters are valid
    assert isinstance(data, defaultdict), 'The data extracted from this file must be stored in a dictionary'
    assert isinstance(subplot_rows, int), 'The number of rows for the subplot must be an integer'
    assert isinstance(subplot_columns, int), 'The number of columns for the subplot must be an integer'

    # initialize empty lists
    texts = []
    sentiment_distributions = []

    # obtain the word count dictionary of a file
    word_count_dict = data['wordcount']

    # initialize a sentiment intensity analyzer
    sia = SentimentIntensityAnalyzer()

    # grab the words from each file and compile them into one string per file
    for text, word_count in word_count_dict.items():
        words = convert_file_to_string(word_count, max_words=max_words)

        # calculate the sentiment distributions (negative vs. neutral vs. positive) for each file and store them in a
        # dictionary
        sentiment_distribution = sia.polarity_scores(words)

        # store the names of the files as well as their sentiment distribution dictionaries
        texts.append(text)
        sentiment_distributions.append(sentiment_distribution)

    # Creates subplots showing the sentiment score distributions (positive vs. neutral vs. negative) of each file as
    # bar charts
    for i in range(len(texts)):
        plt.subplot(subplot_rows, subplot_columns, i + 1)

        for sentiment, score in sentiment_distributions[i].items():
            # displays the negative score of a text file
            if sentiment == 'neg':
                plt.barh('Negative', score, label='Negative', color='firebrick')

            # displays the neutral score of a text file
            elif sentiment == 'neu':
                plt.barh('Neutral', score, label='Neutral', color='gold')

            # displays the positive score of a text file
            elif sentiment == 'pos':
                plt.barh('Positive', score, label='Positive', color='limegreen')

            # Each subplot is labeled based on the text they are representing
            plt.gca().title.set_text('Sentiment Distributions For "' + texts[i] + '"')

    # Gives the plot a title
    plt.suptitle('Overall Sentiment Distributions')

    # resizes the graph to ensure that it can be clearly read
    plt.gcf().set_size_inches(50, 14)

    # adjusts spacing between graphs
    plt.subplots_adjust(wspace=.8, hspace=.8)

    # display the bar charts
    plt.show()


def avgwlength_boxplot(data):
    """ Creates a boxplot summarizing the word length distributions of each registered file
    Citation:
    https://www.tutorialspoint.com/creating-multiple-boxplots-on-the-same-graph-from-a-dictionary-using-matplotlib
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
    Returns:
        None (just generates a boxplot in one visualization representing all the files)
    """
    # Making sure the type of the inputted parameter is valid
    assert isinstance(data, defaultdict), 'The data extracted from this file must be stored in a dictionary'

    # obtain the word length dictionary
    word_length_dict = data['wordlengthlist']

    # set the figure size
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True

    # initialize a figure for the subplots
    fig, ax = plt.subplots()

    # plot the box plots summarizing the distribution of the word lengths with labels indicating the song they represent
    ax.boxplot(word_length_dict.values())
    ax.set_xticklabels(word_length_dict.keys(), rotation=90, fontsize=5)
    plt.xlabel('Name of Song')
    plt.ylabel('Word Length Distributions')
    plt.title('Word Length Distributions for the Different Songs')

    # make the boxplot show
    plt.show()


def avgwlength_bar(data):
    """ Creates a bar chart comparing the average word length for each of the files
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
    Returns:
        None (just generates a bar chart)
    """
    # Ensuring that the inputted parameters are of the correct type
    assert isinstance(data, defaultdict), 'The data extracted from this file must be stored in a dictionary'

    # obtain the average word length dictionary
    avg_wordl_dict = data['avgwordlength']

    # get the labels and average word length values and store them as separate lists
    label = list(avg_wordl_dict.keys())
    value = list(avg_wordl_dict.values())

    # set the figure size
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True

    # plot the bar chart, style the x ticks, label the axes and title
    plt.bar(range(len(avg_wordl_dict)), value, tick_label=label)
    plt.xticks(rotation=90, fontsize=5)
    plt.xlabel('Name of Song')
    plt.ylabel('Average Word Length')
    plt.title('Average Word Lengths for the Different Songs')

    # make the chart show
    plt.show()


def total_wordl_boxplot(data):
    """ Create a boxplot that presents the distribution of the word lengths for the words from all the files combined
    Args:
        data (dict): data extracted from the file as a dictionary attribute--> raw data
    Returns:
        None (just generates a boxplot)
    """
    # Checking the inputted parameter is of the correct type
    assert isinstance(data, defaultdict), 'The data extracted from this file must be stored in a dictionary'

    # obtain the word length list dictionary
    word_length_dict = data['wordlengthlist']

    # get just the word lengths
    total_wl_list = list(word_length_dict.values())

    # turn the 2D list into a 1D list for plotting purposes
    total_wl_list = [item for sublist in total_wl_list for item in sublist]

    # set the figure size
    plt.figure(figsize=(10, 7))

    # create the box plot, set the axes and title
    plt.boxplot(total_wl_list)
    plt.ylabel('Word Length')
    plt.title('Word Length Distribution for All Files Combined')

    # show plot
    plt.show()
