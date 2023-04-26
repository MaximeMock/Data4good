import os, sys
import pandas as pd
import plotly.graph_objects as go

# Open a file
path = os.getcwd()
dirs = os.listdir( path +'/Data/')
dirs.sort()

#print(dirs)

def read_electricity_data(date_debut: str, date_fin: str):
    """
    Reads electricity data from CSV files located in the 'Data' directory.
    Returns a list of Pandas DataFrames containing data between the start date and end date specified.
    Args:
    date_debut (str): Start date in 'YYYY-MM' format.
    date_fin (str): End date in 'YYYY-MM' format.
    Returns:
    List[pd.DataFrame]: A list of Pandas DataFrames containing electricity data for the specified period.
    """
    df_list = list()
    for file in dirs:
        
        #print('---------------------------',file, '-------------------------')
        
        if 'Electricite' in file:
            print(file)
            df = pd.read_csv('Data/'+file,delimiter=';').drop(0).sort_values('Période')
            #print(df[-1:])
            df = df.loc[(df.loc[:,'Période'] >= date_debut) & (df.loc[:,'Période'] <= date_fin)].reset_index(drop=True)
            df['Période']= pd.to_datetime(df['Période'], format='%Y-%m')
            for column in df.columns:
                if column!='Période':
                    df[column] = df[column].astype(float)
            df_list.append(df)
    #print(len(df_list))
    return df_list

def read_petrole_data(date_debut, date_fin):
    """
    Reads petrole data from CSV files located in the 'Data' directory.
    Returns a list of Pandas DataFrames containing data between the start date and end date specified.
    Args:
    date_debut (str): Start date in 'YYYY-MM-DD' format.
    date_fin (str): End date in 'YYYY-MM-DD' format.
    Returns:
    List[pd.DataFrame]: A list of Pandas DataFrames containing pretrole data for the specified period.
    """
    df_list = list()
    for file in os.listdir('Data/'):        #print('---------------------------',file, '-------------------------') 
        if 'Petrole' in file:
            print(file)
            df = pd.read_csv('Data/'+file,delimiter=';')
            df = df.iloc[1:]
            df['Période']= pd.to_datetime(df['Période'], format='%Y-%m-%d ')
            df = df.set_index('Période')
            df = df[df.columns].astype(float)
            df = df.loc[date_debut : date_fin]
            df_list.append(df)
    print(len(df_list))
    return df_list

def plot_from_df(df,labels, title, x_title, y_title, save=False, path_to_save=''):
    """
    Plots data from a Pandas DataFrame using Plotly.
    Args:
    df (pd.DataFrame): The Pandas DataFrame containing data to be plotted.
    labels (List[str]): A list of labels for the data series to be plotted.
    title (str): The title of the plot.
    x_title (str): The label of the x-axis.
    y_title (str): The label of the y-axis.
    Returns:
    None.
    """
    list_columns = df.columns[1:].to_list()
        
    fig = go.Figure()
    i=0
    for column in list_columns:
        fig.add_trace(go.Scatter(x=df.Période, y=df[column], name=labels[i]))
        i= i+1
    fig.add_vrect(x0='2020-03-11', x1='2022-02-24', line_width=0, fillcolor="red", opacity=0.1, annotation_text='Crise liée au COVID-19', annotation_position='inside top left')
    fig.add_vrect(x0='2022-02-24', x1='2023-04-01', line_width=0, fillcolor="blue", opacity=0.1, annotation_text='Guerre en Ukraine', annotation_position='inside top left')
    fig.update_layout(title_text=title, legend_title_text = "Légende :", width=1000, height=600, template='simple_white')
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=y_title)
    if not save:
            fig.show()
    if save:
        fig.write_image(path_to_save)

def plot_from_df_with_list_col(df: pd.DataFrame, list_columns: list(), labels: list(), title: str, x_title: str, y_title: str, save: bool = False, path_to_save: str = '') :
    """
    Plots data from a Pandas DataFrame using Plotly.
    Args:
    df (pd.DataFrame): The Pandas DataFrame containing data to be plotted.
    list_columns (List[str]): A list of column names to be plotted.
    labels (List[str]): A list of labels for the data series to be plotted.
    title (str): The title of the plot.
    x_title (str): The label of the x-axis.
    y_title (str): The label of the y-axis.
    save (bool): A flag indicating whether to save the plot or display it. Default is False.
    path_to_save (str): The path where the plot should be saved if `save` is True. Default is an empty string.
    Returns:
    None.
    """
            
    fig = go.Figure()
    i=0
    for column in list_columns:
        fig.add_trace(go.Scatter(x=df.Période, y=df[column], name=labels[i]))
        i= i+1
    fig.add_vrect(x0='2020-03-11', x1='2022-02-24', line_width=0, fillcolor="red", opacity=0.1, annotation_text='Crise liée au COVID-19', annotation_position='inside top left')
    fig.add_vrect(x0='2022-02-24', x1='2023-04-01', line_width=0, fillcolor="blue", opacity=0.1, annotation_text='Guerre en Ukraine', annotation_position='inside top left')
    fig.update_layout(title_text=title, legend_title_text = "Légende :", width=1000, height=600, template='simple_white')
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=y_title)
    if not save:
            fig.show()
    if save:
        fig.write_image(path_to_save)

def plot_first_column_from_df1_df2(df1: pd.DataFrame,df2: pd.DataFrame,labels: list(), title: str, x_title: str, y_title: str, correction: float(), save: bool=False, path_to_save: str=''):
    """
    Plots the first column of two input dataframes on the same plot.
    Args:
    - df1 (pandas.DataFrame): First dataframe to be plotted.
    - df2 (pandas.DataFrame): Second dataframe to be plotted.
    - labels (list): List containing two string labels for the two dataframes.
    - title (str): Title of the plot.
    - x_title (str): Title of the x-axis.
    - y_title (str): Title of the y-axis.
    - correction (float): Factor by which to divide the first column of df1 for normalization.
    - save (bool, optional): Whether or not to save the plot to a file. Defaults to False.
    - path_to_save (str, optional): Path to save the plot. Only used if save is True. Defaults to ''.
    Returns:
    - None. Displays the plot or saves it to a file, depending on the save argument.
    """
    list_columns1 = df1.columns[1:].to_list()
    list_columns2 = df2.columns[1:].to_list()
   
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1.Période, y=df1[list_columns1[0]]/correction, name=labels[0]))
    fig.add_trace(go.Scatter(x=df2.Période, y=df2[list_columns2[0]], name=labels[1]))
    fig.add_vrect(x0='2020-03-11', x1='2022-02-24', line_width=0, fillcolor="red", opacity=0.1, annotation_text='Crise liée au COVID-19', annotation_position='inside top left')
    fig.add_vrect(x0='2022-02-24', x1='2023-04-01', line_width=0, fillcolor="blue", opacity=0.1, annotation_text='Guerre en Ukraine', annotation_position='inside top left')
    fig.update_layout(title_text=title, legend_title_text = "Légende :", width=1000, height=600, template='simple_white')
    fig.update_xaxes(title_text=x_title)
    fig.update_yaxes(title_text=y_title)
    if not save:
            fig.show()
    if save:
        fig.write_image(path_to_save)
        
        
def scatter_plot_2lines(x1, y1, label_1, x_label, y_label, title, x2 = None, y2 = None, label_2 = None, save=False, path_to_save=''):
    '''
    Save or plot a 1 or 2 lines scatter plot 
    
    Input :
    x1 : pd.Series, X data for first line
    x2 : pd.Series, X data for second line
    y1 : pd.Series, Y data for first line
    y2 : pd.Series, Y data for second line
    label_1 : str, Name for first line
    label_2 : str, Name for second line
    x_label : str, Name for X axis
    y_label : str, Name for Y axis
    save : Bool, Allow to save or not the plot
    path_to_save : str, path where the plot will be stored
    
    Return :
    None
    '''
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1.astype(float), name=label_1))
    if isinstance(y2, pd.Series) == True:
        fig.add_trace(go.Scatter(x=x2, y=y2.astype(float), name=label_2))

    fig.add_vrect(x0='2020-03-11', x1='2022-02-24', line_width=0, fillcolor="red", opacity=0.1, annotation_text='Crise liée au COVID-19', annotation_position='inside top left')
    fig.add_vrect(x0='2022-02-24', x1='2022-12-31', line_width=0, fillcolor="blue", opacity=0.1, annotation_text='Guerre en Ukraine', annotation_position='inside top left')
    fig.update_layout(title_text=title, title_x=0.5, legend_title_text = "Légende :", width=800, height=400, template='plotly_white')
    fig.update_xaxes(title_text=x_label, showgrid=False, showline = True, linecolor = '#000000')
    fig.update_yaxes(title_text=y_label, showgrid=False, showline = True, linecolor = '#000000')
    if isinstance(y2, pd.Series) == True:
        max_val = max(max(y1), max(y2))
    else:
        max_val = max(y1)
    
    max_val = max_val+max_val*0.10
    fig.update_layout(yaxis=dict(range=[0, max_val]))
    if not save:
        fig.show()
    if save:
        fig.write_image(path_to_save)
        

def ouverture_df(path, date_debut, date_fin):
    '''
    Open a file datas in pandas dataframe
        Input :
        path (str): path of the file to open
        date_debut (str): starting date of the period to treat
        date_fin (str): ending date of the period to treat
        Return :
        Dataframe pandas
    '''
    df = pd.read_csv(path, sep=';').drop(0).sort_values('Période')
    df = df.loc[(df.loc[:,'Période'] >= date_debut) & (df.loc[:,'Période'] <= date_fin)].reset_index(drop=True)
    df.index = pd.to_datetime(df.Période)
    return df


def scatter_plot(x1, y1, label_1, title, x_label, y_label, save=False, path_to_save=''):
    '''
    Save or plot a 2 lines scatter plot 
    
    Input :
    x1 : pd.Series, X data for first line
    y1 : pd.Series, Y data for first line
    label_1 : str, Name for first line
    x_label : str, Name for X axis
    y_label : str, Name for Y axis
    save : Bool, Allow to save or not the plot
    path_to_save : str, path where the plot will be stored
    
    Return :
    None
    '''
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1.astype(float), name=label_1))
    fig.add_vrect(x0='2020-03-11', x1='2022-02-24', line_width=0, fillcolor="red", opacity=0.1, annotation_text='Crise liée au COVID-19', annotation_position='inside top left')
    fig.add_vrect(x0='2022-02-24', x1='2022-12-31', line_width=0, fillcolor="blue", opacity=0.1, annotation_text='Guerre en Ukraine', annotation_position='inside top left')
    fig.update_layout(title_text=title, title_x=0.5, legend_title_text = "Légende :", width=800, height=400, template='plotly_white')
    fig.update_xaxes(title_text=x_label, showgrid=False, showline = True, linecolor = '#000000')
    fig.update_yaxes(title_text=y_label, showgrid=False, showline = True, linecolor = '#000000')
    if not save:
        fig.show()
    if save:
        fig.write_image(path_to_save)
        
        
def scatter_plot_2lines_2y_axis(x1, y1, x2, y2, label_1, label_2, title, x_label, y_label, save=False, path_to_save=''):
    '''
    Save or plot a 2 lines scatter plot 
    
    Input :
    x1 : pd.Series, X data for first line
    x2 : pd.Series, X data for second line
    y1 : pd.Series, Y data for first line
    y2 : pd.Series, Y data for second line
    label_1 : str, Name for first line
    label_2 : str, Name for second line
    x_label : str, Name for X axis
    y_label : str, Name for Y axis
    save : Bool, Allow to save or not the plot
    path_to_save : str, path where the plot will be stored
    
    Return :
    None
    '''
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x1, y=y1.astype(float), name=label_1), secondary_y=False)
    fig.add_trace(go.Scatter(x=x2, y=y2.astype(float), name=label_2), secondary_y=True)

    fig.add_vrect(x0='2020-03-11', x1='2022-02-24', line_width=0, fillcolor="red", opacity=0.1, annotation_text='Crise liée au COVID-19', annotation_position='inside top left')
    fig.add_vrect(x0='2022-02-24', x1='2022-12-31', line_width=0, fillcolor="blue", opacity=0.1, annotation_text='Guerre en Ukraine', annotation_position='inside top left')
    fig.update_layout(title_text=title, title_x=0.5, legend_title_text = "Légende :", width=800, height=400, template='plotly_white')
    fig.update_xaxes(title_text=x_label, showgrid=False, showline = True, linecolor = '#000000')
    fig.update_yaxes(title_text=y_label, showgrid=False, showline = True, linecolor = '#000000', secondary_y=False)
    fig.update_yaxes(title_text=y_label, showgrid=False, showline = True, linecolor = '#000000', secondary_y=True)

    if not save:
        fig.show()
    if save:
        fig.write_image(path_to_save)
        

def plot_n_scatter_2axis(x, y_1, ys, label_1, labels, title, x_label, y_label, save=False, path_to_save=''):
    '''
    
    '''
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x, y=y_1, name=label_1),secondary_y=False)
    for idx, (name, series) in enumerate(ys):
        fig.add_trace(go.Scatter(x=x, y=series, name=labels[idx]), secondary_y=True)
        
    fig.add_vrect(x0='2020-03-11', x1='2022-02-24', line_width=0, fillcolor="red", opacity=0.1, annotation_text='Crise liée au COVID-19', annotation_position='inside top left')
    fig.add_vrect(x0='2022-02-24', x1='2022-12-31', line_width=0, fillcolor="blue", opacity=0.1, annotation_text='Guerre en Ukraine', annotation_position='inside top left')
    fig.update_layout(title_text=title, legend_title_text = "Légende :", width=800, height=400, template='simple_white', legend=dict(x=1.1))
    fig.update_xaxes(title_text=x_label, showgrid=False, showline = True, linecolor = '#000000')
    fig.update_yaxes(title_text=y_label, showgrid=False, showline = True, linecolor = '#000000', secondary_y=False)

    fig.update_yaxes(title_text=y_label, showgrid=False, showline = True, linecolor = '#000000', secondary_y=True)
    if not save:
        fig.show()
    if save:
        fig.write_image(path_to_save)
        

def barchart(df, year1, year2, name1, name2, title, x_label, y_label):
    '''
    Plot a barchart plot to compare 2 years.
    Input :
    df (pd.DataFrame) : Dataframe of the data you want to plot
    year1 (str) : First year you want to look at
    year2 (str) : Second year you want to look at
    name1 (str) : Name of the first value
    name2 (str) : Name of the second value
    title (str) : Title of the graph
    x_label (str) : Name for X axis
    y_label (str) : Name for Y axis
    
    Return :
    None    
    '''
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index,
        y=df[year1]*100,
        name=name1,
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=df.index,
        y=df[year2]*100,
        name=name2,
        marker_color='lightsalmon'
    ))

    fig.update_layout(title_text=title, legend_title_text = "Légende :", width=800, height=400, template='simple_white')
    fig.update_xaxes(title_text=x_label)
    fig.update_yaxes(title_text=y_label)

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.show()
    

def BubbleCloud(df, labels, values, label_highlight = None):
    '''
    Plot a bubblecloud.
    Input :
    df (pd.DataFrame) : Dataframe of the data you want to plot
    labels (str) : Name of the column of the DataFrame containing labels of the data
    values (str) : Name of the column of the DataFrame containing labels of the data
    label_highlight (str) : Name of the label(s) you want to highlight
    
    Return :
    None    
    '''
    n_colors = len(df[labels])
    get_colors = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    colours = get_colors(n_colors)
    plot_labels = [f'{i} \n({str(j)} ktep)' for i,j in zip(df[labels], 
                                                    df[values])]
    circle_plot = circlify.circlify(df[values].tolist(), 
                               target_enclosure=circlify.Circle(x=0, y=0))

    # Note that circle_plot starts from the smallest to the largest, 
    # so we have to reverse the list
    circle_plot.reverse()
    fig, axs = plt.subplots(figsize=(15, 15))
    # Find axis boundaries
    lim = max(max(abs(circle.x) + circle.r, 
              abs(circle.y) + circle.r,) 
          for circle in circle_plot)
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    # Display circles.
    for circle, colour, label in zip(circle_plot, colours, plot_labels):
        x, y, r = circle
        axs.add_patch(plt.Circle((x, y), r, linewidth=1, color = colour,
                             edgecolor='grey'))
        if label_highlight in label:
            plt.annotate(label, (x, y), color = 'black', fontsize = r*75, va='center', ha='center', fontweight='bold')
        else:
            plt.annotate(label, (x, y), color = 'white', fontsize = r*75, va='center', ha='center', fontweight='bold')
    plt.axis('off')
    plt.title('Production de pétrole en 2021', fontsize = 30)
    plt.show()