import os, sys
import pandas as pd
import plotly.graph_objects as go

path = os.getcwd()
dirs = os.listdir( path +'/Data/RTE')
dirs.sort()
i = 0
for file in dirs:
    #print(file)
    print(i)
    df = pd.read_csv('Data/RTE/'+file,encoding="ISO-8859-1", sep='\t', low_memory=False, index_col=0, header = [0,1])
    # headers = pd.read_csv('Data/RTE/'+file, header=None, nrows=2,
    #                   index_col=0, keep_default_na=False).values.tolist()
    # df = pd.read_csv('Data/RTE/'+file, encoding="ISO-8859-1", header=[0, 1], index_col=0)
    # df.columns = pd.MultiIndex.from_arrays(headers)
    print(df.head(5))

    i=i+1
    #print(df.info())