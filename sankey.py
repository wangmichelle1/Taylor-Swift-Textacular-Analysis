"""
Jethro R. Lee and Michelle Wang
DS 3500
Reusable NLP Library - HW3
2/27/2023

sankey.py: A reusable library for Sankey visualization
"""
# import necessary libraries
import plotly.graph_objects as go
import pandas as pd


def _code_mapping(df, src, targ):
    """ Assigns specific values within columns of a dataframe to integers that can be linked via a Sankey chart
    Args:
        df (pd.DataFrame): input Pandas dataframe
        src (str): input name of column containing the source values of the Sankey diagram
        targ (str): input name of column containing the target values of the Sankey diagram

    Returns:
        df (pd.DataFrame): an updated version of the inputted dataframe in which each value is mapped to one integer
        labels (list of str): labels used for the bars of the Sankey diagram
    """
    # Checking that the inputted parameters are of a valid type
    assert isinstance(df, pd.DataFrame), 'The inputted dataframe must be a Pandas dataframe'
    assert isinstance(src, str), 'The name of the column containing the source values of the Sankey diagram must be ' \
                                 'inputted as a string'
    assert isinstance(targ, str), 'The name of the column containing the target values of the Sankey diagram must be ' \
                                  'inputted as a string'

    # Get distinct labels
    data_types_dict = {src: str, targ: str}
    df = df.astype(data_types_dict)
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    # Get integer codes
    codes = list(range(len(labels)))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels


def _prepare_sankey_data(df, src, targ, threshold=None):
    """ Adjusts a dataframe so that it is suited for making a Sankey diagram with
    Args:
        df (pd.DataFrame): input Pandas dataframe
        src (str): input name of column containing the source values of the Sankey diagram
        targ (str): input name of column containing the target values of the Sankey diagram
        threshold (int): minimum number of instances that a combination of values must have to be shown on the diagram

    Returns:
        df (pd.DataFrame): updated version of the inputted Pandas dataframe, which contains no rows where the count
                           for rows with a certain combination of values is below a threshold (if specified)
    """
    # Checking that the inputted parameters are of a valid type
    assert isinstance(df, pd.DataFrame), 'The inputted dataframe must be a Pandas dataframe'
    assert isinstance(src, str), 'The name of the column containing the source values of the Sankey diagram must be ' \
                                 'inputted as a string'
    assert isinstance(targ, str), 'The name of the column containing the target values of the Sankey diagram must be ' \
                                  'inputted as a string'
    assert isinstance(threshold, int), 'The minimum number of instances that a combination of values must have to be ' \
                                       'shown on the diagram must be entered as an integer'

    # Aggregation: counts the number of artists grouped by both the source value and target value
    df = df.groupby([src, targ]).size().reset_index(name="Counts")

    # filters out rows where the count is below a certain threshold
    if threshold is not None:
        df = df[df['Counts'] > threshold]
        df = df.astype(str)

    return df


def make_sankey(df, threshold, *cols, vals=None, **kwargs):
    """ Create a Sankey diagram linking src values to target values with thickness vals
    Args:
        df (pd.DataFrame): input Pandas dataframe
        threshold (int): minimum number of instances needed for a combination of values to be shown on the diagram
        *cols (tuple): names of columns (str) with the values in df for the Sankey diagram layers. The columns are shown
                       from left to right based on the order they are inputted (1st inputted column = left-most layer)
        vals (series): series for thickness of each bar on the Sankey diagram
        **kwargs (dict): additional parameters (strings linked to float) to personalize the Sankey chart further

    Returns:
        Nothing, just generates and presents a Sankey diagram
    """
    # Checking that the inputted parameters are of a valid type and/or value
    assert isinstance(df, pd.DataFrame), 'The inputted dataframe must be a Pandas dataframe'
    assert isinstance(threshold, int), 'The minimum number of instances that a combination of values must have to be ' \
                                       'shown on the diagram must be entered as an integer'
    assert all(isinstance(col, str) for col in cols), 'The columns used for the Sankey diagram must be specified as ' \
                                                      'strings'
    assert len(cols) >= 2, 'You must specify at least 2 columns to generate the Sankey diagram with'

    # Stacks all the data indicated by the inputted columns into one dataframe
    sankey_data = df[[cols[0], cols[1]]]
    sankey_data.columns = ['src', 'targ']

    for i in range(1, (len(cols) - 1)):
        stacked = df[[cols[i], cols[i + 1]]]
        stacked.columns = ['src', 'targ']
        sankey_data = pd.concat([sankey_data, stacked], axis=0)

    # Removes any rows where the value associated with a combination of items is below a threshold (if specified)
    sankey_data = _prepare_sankey_data(sankey_data, 'src', 'targ', threshold=threshold)

    # Assigns values to be used on the Sankey chart between two nodes if they aren't given
    if vals is None:
        vals = sankey_data['Counts']
    else:
        assert vals.dtype == 'int64', 'The thickness of the bars must be specified as integers'

    # Prepares the aesthetics of the Sankey diagram (e.g. links, labels, optional padding, other specifics in kwargs)
    sankey_data, labels = _code_mapping(sankey_data, 'src', 'targ')
    link = {'source': sankey_data['src'], 'target': sankey_data['targ'], 'value': vals}
    pad = kwargs.get('pad', 50)
    width = kwargs.get('width', 800)
    height = kwargs.get('height', 800)

    # Prepares the nodes and generates the Sankey chart
    node = {'label': labels, 'pad': pad}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.update_layout(
        autosize=False,
        width=width,
        height=height)
    fig.show()
