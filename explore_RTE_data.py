import os, sys
import pandas as pd
import plotly.graph_objects as go
from module_read_plot_electricity_rte_data import dirs, read_rte_data, plot_subplot_resources, list_series_data

def main():
    print("Hello World!")
    df = read_rte_data()
    print(df)
    list_resource =["Gaz", "Nucléaire", "Fioul", "Charbon"]
    list_series = list_series_data(df, list_resource)
    #print(list_series)
    plot_subplot_resources(list_series,list_resource, save=True, path_to_save='images/rte.png')
 
        
if __name__ == "__main__":
    main()