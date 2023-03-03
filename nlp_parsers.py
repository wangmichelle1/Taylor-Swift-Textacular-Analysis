"""
Jethro R. Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

nlp_parsers.py: JSON, CSV, Excel, and optional custom parsers to store the contents of a file into a list of its words
"""
# import necessary libraries
import pandas as pd


def custom_parser(filename, text_column, parser):
    """ Reads in a file to make a Pandas dataframe out of and returns a list of only the words of interest
    Args:
        filename (str): name of the file of interest
        text_column (str): name of column of interest from the dataframe (which contains the texts)
        parser (str): type of custom parser to be used
    Returns:
        clean_words_list (list): list of words (str) from the file without whitespace characters

    These parsers are for non-txt files only.

    The default parsers contained in this function include "CSV" for CSV files, "JSON" for JSON files, and "Excel" for
    Excel files. Any others with different names are assumed to be custom and must be imported.
    """
    assert isinstance(filename, str), 'File name must be specified as a string'
    assert filename[-3:] in ('csv', 'txt', 'son', 'xls', 'lsx', 'lsm'), 'File type unsupported'
    assert isinstance(text_column, str), 'The column of the new dataframe which contains the texts must be specified ' \
                                         'as a string'

    # initialize empty list
    clean_words_list = []

    # read in JSON file into a dataframe
    if filename[-3:] == 'json':
        df = pd.read_json(filename)

    # read in CSV file into a dataframe
    elif filename[-3:] == 'csv':
        df = pd.read_csv(filename)

    # read in Excel file into a dataframe
    else:
        df = pd.read_excel(filename)

    # get the column that has the texts
    df_text = df[text_column]

    # turn the column of texts into a list
    words_list = list(df_text)

    # parse a JSON, CSV, or Excel file with an appropriate default parser
    if parser.lower() in ['json', 'csv', 'excel']:
        for word in words_list:
            # remove leading and trailing white-spaces
            word = word.strip()
            clean_words_list.append(word)
    else:
        # If a user wants to use a custom parser, make sure they input a string indicating a callable function
        assert (callable(parser)), "The name of your parser must be a callable function. Don't forget to import it " \
                                   "if necessary"
        # parse a JSON, CSV, or Excel file with a custom parser
        clean_words_list = parser(words_list)
        # Ensures the custom parser returns a list of words
        assert isinstance(clean_words_list, list), 'The custom parser must return a list of words'
        assert all(isinstance(clean_word, str) for clean_word in clean_words_list), 'The custom parser must return a ' \
                                                                                    'list of words '

    return clean_words_list
