"""
Jethro R. Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

exception.py: A set of framework-specific exception classes
"""


class DataResultsError(Exception):
    """ A user-defined exception for signaling an issue with creating a dictionary containing the word frequencies,
    overall word count, world length list, and average word lengths of a file
    Attributes:
        clean_words (list): list of words of interest that are clean
        msg (str): message shown to user
    """
    def __init__(self, clean_words, msg=''):
        super().__init__('A dictionary containing the word frequencies, overall word count, world length list, and '
                         'average word lengths could not be made for this file')
        self.clean_words = clean_words
        self.msg = msg


class StopWordError(Exception):
    """ A user-defined exception for signaling an issue with filtering out the stop words from a list of words
    Attributes:
        words (str): list of words that may have stop words
        msg (str): message shown to user
    """
    def __init__(self, words, msg=''):
        super().__init__('Stop words could not be filtered out')
        self.words = words
        self.msg = msg


class DefaultParsingError(Exception):
    """ A user-defined exception for signaling an issue with the default parsing
    Attributes:
        filename(str): name of file
        msg (str): message shown to user
    """
    def __init__(self, filename, msg=''):
        super().__init__('Default parsing unsuccessful')
        self.filename = filename
        self.msg = msg


class SaveResultsError(Exception):
    """A user-defined exception for signaling an issue with integrating parsing results into the internal state
    Attributes:
        label (str): unique label for a parsed text file
        results (dict): the data extracted from the file as a dictionary attribute--> raw data
        msg (str): message shown to user
    """
    def __init__(self, label, results, msg=''):
        super().__init__('Parsing results could not be saved into the internal state')
        self.label = label
        self.results = results
        self.msg = msg


class ParserError(Exception):
    """ A user-defined exception for signaling a parser error issue
    Attributes:
        filename (str): name of the file of interest
        label (str): optional label for file
        parser (str): optional type of parser to be used
        text_column (str): name of column that has the text of interest
        msg (str): message shown to user
    """
    def __init__(self, filename, label=None, parser=None, text_column='text', msg=''):
        super().__init__('Issue with parsing the file')
        self.filename = filename
        self.label = label
        self.parser = parser
        self.text_column = text_column
        self.msg = msg


class LoadStopWordError(Exception):
    """ A user-defined exception for an issue with loading the stop words
    Attributes:
        stopfile (str): optional txt file containing stop words, or common words that will get filtered
        parser (str): optional parser to be used
        msg (str): message shown to user
    """
    def __init__(self, stopfile=None, parser=None, msg=''):
        super().__init__('Stop words could not be loaded')
        self.stopfile = stopfile
        self.parser = parser
        self.msg = msg


class LoadVisualizationError(Exception):
    """ A user-defined exception for an issue with loading a visualization into the internal state
    Attributes:
        name (str): name of visualization
        vizfunc (function): name of function to execute the visualization
        msg (str): message shown to user
    """
    def __init__(self, name, vizfunc, msg=''):
        super().__init__(name, 'could not be integrated into the internal state')
        self.name = name
        self.vizfunc = vizfunc
        self.msg = msg


class VisualizeError(Exception):
    """ A user-defined exception for an issue with plotting the visualization(s)
    Attributes:
        name (str): optional parameter for the name of a visualization
        msg (str): message shown to user
    """
    def __init__(self, name=None, msg=''):
        super().__init__('Visualization(s) could not be plotted')
        self.name = name
        self.msg = msg
