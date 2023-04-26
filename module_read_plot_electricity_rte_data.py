
import os, sys
import pandas as pd
import plotly.graph_objects as go
import io
from dateutil import parser
import scipy
from plotly.subplots import make_subplots
import plotly.graph_objects as go

path = os.getcwd()
dirs = os.listdir( path +'/Data/RTE')
dirs.sort()

def change_col_to_point(x):
    """
    Converts a string or numeric value to a float using a dot as the decimal separator.

    Args:
        x: A string or numeric value.

    Returns:
        The value of x converted to a float with a dot as the decimal separator. If x is already a float,
        returns the original value.

    Raises:
        TypeError: If x is not a string or numeric value.

    Examples:
        >>> change_col_to_point('3,14')
        3.14

        >>> change_col_to_point(5)
        5.0

        >>> change_col_to_point('2.718')
        2.718

        >>> change_col_to_point('hello')
        Traceback (most recent call last):
            ...
        TypeError: invalid type: str, expected string or numeric value
    """
    if type(x) is str:
        x = x.replace(',', '.')
        return float(x)
    else:
        return float(x)
    

def read_rte_data():
    """
    Reads RTE data files from the 'Data/RTE' directory and returns a cleaned and aggregated pandas DataFrame.

    Returns:
        A pandas DataFrame containing the aggregated data from all files in the 'Data/RTE' directory.

    Raises:
        FileNotFoundError: If the 'Data/RTE' directory is not found.

    Examples:
        >>> df = read_rte_data()
        >>> print(df.head())
                       D1      D2      D3  ...      D7      D8      D9
        2013-12-31  39020  42489.2  15418  ...  3955.5  2590.5  2975.5
        2014-01-01  39520  42961.2  15574  ...  3862.0  2610.5  2999.5
        2014-01-02  38498  42104.0  15309  ...  3796.5  2579.5  2976.5
        2014-01-03  38554  41872.0  15323  ...  3794.0  2576.5  2981.5
        2014-01-04  36020  39257.6  14296  ...  3638.0  2469.5  2842.0

    """
    import pandas as pd

    try:
        dirs = os.listdir('Data/RTE')
    except FileNotFoundError:
        raise FileNotFoundError("The 'Data/RTE' directory is not found.")

    df_tot = []
    for file in dirs:
        df = pd.read_csv('Data/RTE/' + file, encoding="ISO-8859-1", sep='\t', low_memory=False, index_col=0, header=[0, 1])
        df = df.replace("*", 0)
        df = df.applymap(change_col_to_point)
        df_tot.append(df)

    df = pd.concat(df_tot)
    df = df.groupby(level=0, axis=1).sum()
    df.index = [i.split('-')[0] for i in df.index]
    df.index = pd.to_datetime(df.index, format='%d/%m/%Y %H:%M')

    return df


def list_series_data(df, list_label):
    """
    Calculates rolling window sums for a list of resources in a pandas DataFrame.

    Args:
        df: A pandas DataFrame containing time series data.
        list_label: A list of resource labels in the DataFrame for which to calculate rolling window sums.

    Returns:
        A list of pandas Series, each containing the rolling window sum for a resource in the input DataFrame.

    Examples:
        >>> df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [6, 7, 8, 9, 10]})
        >>> series_list = list_series_data(df, ['A', 'B'])
        >>> print(series_list[0])
        0     NaN
        1     NaN
        2     6.0
        3    10.5
        4    15.0
        Name: A, dtype: float64
    """
    series_list = []
    for resource in list_label:
        series = df[resource].rolling(700, win_type='triang').sum()
        series_list.append(series)

    return series_list


def plot_subplot_resources(list_series, list_label, save: bool=False, path_to_save: str=''):
    """
    Plots time series data for a list of resources in subplots.

    Args:
        list_series: A list of pandas Series, each containing time series data for a resource.
        list_label: A list of labels corresponding to the resources in `list_series`.
        save: Optional boolean indicating whether to save the plot to a file (default is False).
        path_to_save: Optional string specifying the file path for saving the plot (default is '').

    Returns:
        If `save` is False, displays the plot in the Jupyter notebook. If `save` is True, saves the plot to a file.

    Examples:
        >>> df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [6, 7, 8, 9, 10]})
        >>> series_list = [df['A'], df['B']]
        >>> plot_subplot_resources(series_list, ['Resource A', 'Resource B'])
    """
    fig = make_subplots(rows=len(list_series), cols=1, x_title='Temps en année', y_title="Production d'électricitè (GWh)",)
    
    for i in range(len(list_series)):
        fig.append_trace(go.Scatter(
            x=list_series[i].index,
            y=list_series[i],
            name=list_label[i],
        ), row=i+1, col=1)

    # Add shaded rectangles to highlight important time periods
    fig.add_vrect(x0='2020-03-11', x1='2022-02-24', line_width=0, fillcolor="red", opacity=0.1, annotation_text='Crise liée au COVID-19', annotation_position='inside top left')
    fig.add_vrect(x0='2022-02-24', x1='2023-04-25', line_width=0, fillcolor="blue", opacity=0.1, annotation_text='Guerre en Ukraine', annotation_position='inside top left')

    # Customize the layout of the plot
    fig.update_layout(title_text="Electricitè pour la production a partir des different resourse", legend_title_text="Légende :", width=1200, height=800, template='simple_white')
   
    # Display or save the plot as specified
    if not save:
        fig.show()
    if save:
        fig.write_image(path_to_save)
