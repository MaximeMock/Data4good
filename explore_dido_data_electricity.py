#!/usr/bin/python

import os, sys
import pandas as pd
import plotly.graph_objects as go
# Open a file
path = os.getcwd()
dirs = os.listdir( path +'/Data/')
dirs.sort()

print(dirs)

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


def main():
    print("Hello World!")
    #read_electricity_data()
    df_list = read_electricity_data("2018-01","2023-02")
    
    df_price_menage_electricity = df_list[0]
    df_price_industry_electricity = df_list[1]
    df_electricity_2023 = df_list[2]
    df_summaryze_electricity = df_list[3]


    
    print(df_price_menage_electricity.info())
    
    
    print(df_price_industry_electricity.info())
    print(df_electricity_2023.info())
    print(df_summaryze_electricity.info())
    
    
    
    #print(df_summaryze_electricity.info())
    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------- price menage ------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------

    price_menage_electricity = df_price_menage_electricity.columns[1:].to_list()
    
    labels = ["toutes tranches","tranches DA", "tranches DB", "tranches DC","tranches DD","tranches DE"]
    title = "Prix au détail de l'électricité TTC dans une menage sur la période 2018-2022"
    x_title ='Temps en année'
    y_title = "Prix au détail de l'électricité TTC (€)"
   
    
    plot_from_df(df_price_menage_electricity,labels, title, x_title, y_title, save=True, path_to_save='images/fig1.png')
    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------- price industry ----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------
    #price_industry_electricity = df_price_industry_electricity.columns[1:].to_list()
    labels = ["tranches IA à IF","tranches IA", "tranches IB", "tranches IC","tranches ID","tranches IE", "tranches IF","tranches IG","toutes tranches" ]
    title = "Prix au détail de l'électricité hors TVA dans l'industrie sur la période 2018-2022"
    x_title ='Temps en année'
    y_title = "Prix au détail de l'électricité hors TVA (€)"
    plot_from_df(df_price_industry_electricity,labels, title, x_title, y_title, save=True, path_to_save='images/fig2.png')

    labels = ["Electricite industriels","Electricite dans menage"]
    title = "Prix au détail de l'électricité TTC dans l'industrie et dans le menage sur la période 2018-2022"
    x_title = 'Temps en année'
    y_title = "Prix au détail de l'électricité (€)"
    plot_first_column_from_df1_df2(df_price_industry_electricity,df_price_menage_electricity,labels, title, x_title, y_title, 0.78, save=True, path_to_save='images/fig3.png')

    
    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------- summarize electricity comsumption production import/export 2023 ---------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------
    production_brut = ["Production totale brute d'électricité (en GWh)",
                        "Production brute d'électricité nucléaire (en GWh)",
                        "Production brute d'électricité hydraulique (en GWh)",
                        "Production brute d'électricité éolienne (en GWh)",
                        "Production brute d'électricité photovoltaïque (en GWh)",
                        "Production brute d'électricité thermique (en GWh)"]

    production_net = ["Production totale nette d'électricité (en GWh)",
                        "Production nette d'électricité nucléaire (en GWh)",
                        "Production nette d'électricité hydraulique (en GWh)",
                        "Production nette d'électricité éolienne (en GWh)",
                        "Production nette d'électricité photovoltaïque (en GWh)",
                        "Production nette d'électricité thermique (en GWh)"]
  

    
    labels=["totale","électricité nucléaire","électricité hydraulique","électricité éolienne","électricité photovoltaïque","électricité thermique"]
    title = "Production nette d'électricité (GWh) sur sur la période 2018-2023"
    x_title = 'Temps en année'
    y_title = "Production nette d'électricité (GWh)"
    plot_from_df_with_list_col(df_electricity_2023,production_net, labels, title, x_title, y_title, save=True, path_to_save='images/fig4.png')


    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------- summarize electricity comsumption production import/export --------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------

    production = ["1. Production (brute) d'électricité hydraulique, éolienne et photovoltaïque (en GWh)",
                "1.1 Production brute d'électricité hydraulique (en GWh)",
                "1.2 Production brute d'électricité éolienne (en GWh)",
                "1.3 Production brute d'électricité solaire photovoltaïque (en GWh)",
                "2. Production nucléaire (équivalent primaire à la production, sous forme de chaleur) (en GWh)"]
    import_export = ["3. Solde importateur (importations - exportations) d'électricité (en GWh)",
                "3.1 Importations d'électricité (en GWh)",
                "3.2 Exportations d'électricité (en GWh)"]


    consumption = ["4. Consommation primaire d'énergie nucléaire, hydraulique, éolienne et photovoltaïque brute (en GWh)",
                "5. Consommation d'électricité primaire et d'équivalent primaire d'électricité nucléaire CVC-CJO (en GWh)",
                "6. Consommation d'électricité primaire et d'équivalent primaire d'électricité nucléaire CVS-CVC-CJO (en GWh)"]

    labels =["total: hydraulic - eolic - solar electricity ","hydraulic electricity","eolic electricity","solar electricity","production nuclear"]
    title ="Production (brute) d'électricité renouvable (en GWh) sur la période 2018-2023"
    x_title = 'Temps en année'
    y_title = "Production brute d'électricité (GWh)"
    plot_from_df_with_list_col(df_summaryze_electricity, production, labels, title, x_title, y_title, save=True, path_to_save='images/fig5.png')


    labels =["Total_import_export","import", "export"]
    title = "Import/Export (GWh) sur la période 2018-2023"
    x_title = 'Temps en année'
    y_title = "Import/Export (GWh)"
    plot_from_df_with_list_col(df_summaryze_electricity, import_export, labels, title, x_title, y_title, save=True, path_to_save='images/fig6.png')


    labels =["non nucleiare","nucleiare CVC-CJO", "nucleiare CVS-CVC-CJO"]
    title ="Consommation primaire d'énergie sur la période 2018-2023"
    x_title = 'Temps en année'
    y_title = "Consommation primaire d'énergie (GWh)"
    plot_from_df_with_list_col(df_summaryze_electricity, consumption, labels, title, x_title, y_title, save=True, path_to_save='images/fig7.png')

  

        
if __name__ == "__main__":
    main()
