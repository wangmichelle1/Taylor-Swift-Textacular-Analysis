"""
Jethro Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

nlp.py: Core framework class for NLP Comparative Analysis
"""

from collections import Counter, defaultdict
from nltk.corpus import stopwords
import nlp_parsers as nlp_par
from exception import *


class Nlp:
    """ Core framework class for NLP comparative analysis
    Attributes:
        data (dict): dictionary managing data about the different texts that we register with the framework
        viz (dict): dictionary that maps the name of the visualization to a visualization function
    """

    def __init__(self):
        self.data = defaultdict(dict)
        self.viz = {}

    @staticmethod
    def _data_results(clean_words):
        """ Return data results about an inputted list of words
        Args:
            clean_words (list): list of clean words
        Returns:
            results (dict): dictionary with data about the inputted words
        """
        # make sure the inputted parameters are valid based on their type
        assert isinstance(clean_words, list), 'Clean words must be consolidated into a list'
        assert all(isinstance(clean_word, str) for clean_word in clean_words), 'Clean word list must only contain ' \
                                                                               'strings before getting used'

        try:
            length = 0
            for word in clean_words:
                # add length of word to length variable
                length += len(word)
            # compute average word length
            avg_wl = length / len(clean_words)

            # initialize empty list
            word_length_list = []
            for word in clean_words:
                # append length of word to the new list
                word_length_list.append(len(word))

            # create a dictionary with info on the frequency of each unique word in a file, the word count of the file,
            # the lengths of the words, and the average word length of a file
            results = {
                'wordcount': Counter(clean_words),
                'numwords': len(clean_words),
                'wordlengthlist': word_length_list,
                'avgwordlength': avg_wl
            }
        except Exception as e:
            # throw an error message if the dictionary cannot be created
            raise DataResultsError(clean_words, str(e))

        else:
            # throw a success message if the dictionary gets created
            print('Dictionary containing the word frequencies, overall word count, world length list, and average'
                  'word lengths successfully created')

            return results

    @staticmethod
    def _filter_stopwords(words):
        """ Filter out stop words from a list of given words
        Args:
            words (list): list of words that may have stop words
        Returns:
            clean_words (list): updated version of the inputted list of words without stop words
        """
        # make sure the inputted parameters are valid based on their type
        assert isinstance(words, list), 'Must input the words to be filtered as a list'
        assert all(isinstance(word, str) for word in words), 'Word list must only contain strings before getting ' \
                                                             'filtered'

        try:
            # load the stop words
            stop_words = Nlp._load_stop_words()

            # make all the letters lower case and filter out the file's stop words
            # Citation: https://realpython.com/python-nltk-sentiment-analysis/
            clean_words = [word.lower() for word in words if word.lower() not in stop_words]

        except Exception as e:
            # throws an error message if the stop words cannot be filtered out
            raise StopWordError(words, str(e))

        else:
            # throws a success message if the stop words are filtered out
            print('Stop words successfully filtered out')
            return clean_words

    @staticmethod
    def _default_parser(filename):
        """ Parser that reads in a txt file
        Args:
            filename (str): name of the file of interest
        Returns:
            words (list): list of words (str) from the file
        """
        # Checking that the inputted parameters are valid based on their type
        assert filename[-3:] in ('csv', 'txt', 'son', 'xls', 'lsx', 'lsm'), 'File type unsupported. Must input a' \
                                                                            ' file of the following types: .csv, ' \
                                                                            '.txt, .json, .xls, .xlsx, .xlsm'
        assert isinstance(filename, str), 'File must be inputted as a string'

        try:
            # initialize empty list to store words
            words = []

            # open and read the file of interest
            text_file = open(filename, 'r')
            rows_of_text = text_file.readlines()

            # break the file into words

            # filtering the file
            for row in rows_of_text:
                # remove all break lines
                row = row.replace('\n', '')
                # separate the words from each row in the txt file
                row_words = row.split(' ')

                for word in row_words:
                    # change all letters to lower case
                    word = word.lower()
                    # remove leading and trailing white-spaces
                    word = word.strip()
                    # filter out blank words and possible non-words (e.g., 'words' that start with a number)
                    if word != '' and word[0].isalpha():
                        # remove punctuation from the end of words
                        while not word[-1].isalpha():
                            word = word[:-1]
                        words.append(word)

            # close the file
            text_file.close()

        except Exception as e:
            # throws an error message if the file is not parsed
            raise DefaultParsingError(filename, str(e))

        else:
            # throws a success message if the file is successfully parsed
            print('File is successfully parsed')
            return words

    def _save_results(self, label, results):
        """ Integrate parsing results into internal state
        Args:
            label (str): unique label for a text file that we parsed
            results (dict): the data extracted from the file as a dictionary attribute--> raw data
        Return:
            None (just updates the internal variable, 'data')
        """
        # Ensure the inputted parameters are valid based on their type
        assert isinstance(label, str), 'Label for the text file must be a string'
        assert isinstance(results, dict), 'The data extracted from this file must be stored in a dictionary'

        try:
            # adds the parsing results into the internal state
            for k, v in results.items():
                self.data[k][label] = v

        except Exception as e:
            # throws an error message if the results cannot be saved
            raise SaveResultsError(label, str(e))

    def load_text(self, filename, label=None, parser=None, text_column='text'):
        """ Register a document with the framework
        Args:
            filename (str): name of the file of interest
            label (str): optional label for file
            parser (str): optional type of parser to be used
            text_column (str): name of column that has the text of interest
        Return:
            None, just registers the document
        """
        # Ensuring the inputted parameters are valid based on their type
        assert filename[-3:] in ('csv', 'txt', 'son', 'xls', 'lsx', 'lsm'), 'File type unsupported. Must input a' \
                                                                            ' file of the following types: .csv, ' \
                                                                            '.txt, .json, .xls, .xlsx, .xlsm'
        assert isinstance(filename, str), 'File must be inputted as a string'

        if label is not None:
            assert isinstance(label, str), 'Label for the text file must be a string'

        try:
            # do default parsing of standard .txt file
            if parser is None:
                words = Nlp._default_parser(filename)

            else:
                # checking that the custom parser is inputted as a string
                assert isinstance(parser, str), 'Parser must be a string'

                # do custom parsing for non-.txt files
                words = nlp_par.custom_parser(filename, text_column=text_column, parser=parser)

            # clean the list of words, removing stopwords
            clean_words = Nlp._filter_stopwords(words)
            # compute statistics/calculations regarding the list of words
            results = Nlp._data_results(clean_words)

            # defining the default label for a file
            if label is None:
                label = filename

            # Save/integrate the data we extracted from the file into the internal state of the framework
            self._save_results(label, results)

        except Exception as e:
            # throws an error message if the document cannot be registered into the framework
            raise ParserError(filename, str(e))

        else:
            # throws a success message if the document is successfully registered
            print('Document is successfully registered')

    @staticmethod
    def _load_stop_words(stopfile=None, parser=None):
        """ Load the stop word file and clean it
        Citation: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
        Args:
            stopfile (str): optional txt file containing stop words, or common words, that will get filtered
            parser (str): optional parser to be used
        Returns:
            stop_words (list): list of stopwords based on NLTK library or user-inputted stop file
        """
        try:
            # retrieves a list of stopwords from the NLTK library if none is given
            if stopfile is None:
                stop_words = list(stopwords.words('english'))

            else:
                # ensure that the custom stop file is inputted as a string and that its file type is valid
                assert stopfile[-3:] in ('csv', 'txt', 'son', 'xls', 'lsx', 'lsm'), 'File type unsupported. Must ' \
                                                                                    'input a file of the following ' \
                                                                                    'types: .csv, .txt, .json, .xls, ' \
                                                                                    '.xlsx, .xlsm '
                assert isinstance(stopfile, str), 'File must be inputted as a string'

                if parser is None:
                    # clean the custom stopfile
                    stop_words = Nlp._default_parser(stopfile)
                else:
                    # check that the parser is inputted as a string
                    assert isinstance(parser, str), 'Parser must be inputted as a string'

                    # clean the NLTK stopfile
                    stop_words = nlp_par.custom_parser(stopfile, text_column='text', parser=parser)

        except Exception as e:
            # throws an error message if the stop words cannot get filtered out
            raise LoadStopWordError(stopfile, str(e))

        else:
            # throws a success message if the stop words are filtered out
            print('Stop words successfully loaded')
            return stop_words

    def load_visualization(self, name, vizfunc, *args, **kwargs):
        """ Integrate visualization into internal state
        Args:
            name (str): name of visualization
            vizfunc (function): name of function to execute the visualization
            *args (tuple): unlimited number of defined parameters for the visualization
            **kwargs (dict): unlimited number of undefined parameters for the visualization (parameter name = key,
                             parameter value = value)
        Returns:
            None (just loads the visualization into the internal state)
        """
        # Ensure the inputted parameters are valid based on their type
        assert isinstance(name, str), 'The name of the visualization must be a string'
        assert (callable(vizfunc)), 'You must input a callable function to execute the visualization'

        try:
            # add the visualization into the internal state
            self.viz[name] = (vizfunc, args, kwargs)

        except Exception as e:
            # throws an error message if the visualization cannot get added to the internal state
            raise LoadVisualizationError(vizfunc, str(e))

        else:
            # throws a success message if the visualization is added to the internal state
            print(name, 'is successfully integrated into the internal state')

    def visualize(self, name=None):
        """ Call the vizfunc to plot the visualization(s)
        Args:
            name (str): optional parameter for the name of a visualization
        Returns:
            None (just plots the specified visualization(s))
        """
        try:
            # run all the visualizations
            if name is None:
                for _, v in self.viz.items():
                    vizfunc, args, kwargs = v
                    vizfunc(self.data, *args, **kwargs)

            else:
                # run only the named visualization
                assert isinstance(name, str), 'The name of the visualization must be a string'
                vizfunc, args, kwargs = self.viz[name]
                vizfunc(self.data, *args, **kwargs)

        except Exception as e:
            # throws an error message if the visualization(s) cannot get plotted
            raise VisualizeError(name, str(e))

        else:
            # throws a success message if the visualization gets plotted
            print('Visualization(s) successfully plotted')
