#!/usr/bin/python

import os, sys
import pandas as pd
import plotly.graph_objects as go
# Open a file
path = os.getcwd()
dirs = os.listdir( path +'/Data/')
dirs.sort()

print(dirs)

def read_electricity_data(date_debut, date_fin):
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
    
    fig = go.Figure()
    i=0
    #fig.add_trace(go.Scatter(x=prix_charbon.index, y=prix_charbon.iloc[:,1].astype(float), name='granulés en vrac'))
    for column in price_menage_electricity:
        fig.add_trace(go.Scatter(x=df_price_menage_electricity.Période, y=df_price_menage_electricity[column], name=labels[i]))
        i= i+1
    fig.update_layout(title_text="Prix au détail de l'électricité TTC dans une menage sur la période 2018-2022", legend_title_text = "Légende :", width=800, height=400, template='simple_white')
    fig.update_xaxes(title_text='Temps en année')
    fig.update_yaxes(title_text="Prix au détail de l'électricité TTC (€)")
    fig.show()
    
    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------- price industry ----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------
    price_industry_electricity = df_price_industry_electricity.columns[1:].to_list()
    labels = ["tranches IA à IF","tranches IA", "tranches IB", "tranches IC","tranches ID","tranches IE", "tranches IF","tranches IG","toutes tranches" ]

    fig = go.Figure()
    i=0
    for column in price_industry_electricity:
        fig.add_trace(go.Scatter(x=df_price_industry_electricity.Période, y=df_price_industry_electricity[column], name=labels[i]))
        i= i+1
    fig.update_layout(title_text="Prix au détail de l'électricité hors TVA dans l'industrie sur la période 2018-2022", legend_title_text = "Légende :", width=800, height=400, template='simple_white')
    fig.update_xaxes(title_text='Temps en année')
    fig.update_yaxes(title_text="Prix au détail de l'électricité hors TVA (€)")
    fig.show()

    
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
  

    fig = go.Figure()
    i=0
    for column in production_brut:
        fig.add_trace(go.Scatter(x=df_electricity_2023.Période, y=df_electricity_2023[column], name=labels[i]))
        i= i+1
    fig.update_layout(title_text="Production brute d'électricité (GWh) sur la période 2018-2022", legend_title_text = "Légende :", width=800, height=400, template='simple_white')
    fig.update_xaxes(title_text='Temps en année')
    fig.update_yaxes(title_text="Production brute d'électricité (GWh)")
    fig.show()


    fig = go.Figure()
    i=0
    for column in production_net:
        fig.add_trace(go.Scatter(x=df_electricity_2023.Période, y=df_electricity_2023[column], name=labels[i]))
        i= i+1
    fig.update_layout(title_text="Production nette d'électricité (GWh) sur la période 2018-2022", legend_title_text = "Légende :", width=800, height=400, template='simple_white')
    fig.update_xaxes(title_text='Temps en année')
    fig.update_yaxes(title_text="Production nette d'électricité (GWh)")
    fig.show()


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

    fig = go.Figure()
    i=0
    for column in production:
        fig.add_trace(go.Scatter(x=df_summaryze_electricity.Période, y=df_summaryze_electricity[column], name=labels[i]))
        i= i+1
    fig.update_layout(title_text="Production (brute) d'électricité renouvable (en GWh) sur la période 2018-2022", legend_title_text = "Légende :", width=800, height=400, template='simple_white')
    fig.update_xaxes(title_text='Temps en année')
    fig.update_yaxes(title_text="Production brute d'électricité (GWh)")
    fig.show()

    labels =["Total_import_export","import", "export"]

    fig = go.Figure()
    i=0
    for column in import_export:
        fig.add_trace(go.Scatter(x=df_summaryze_electricity.Période, y=df_summaryze_electricity[column], name=labels[i]))
        i= i+1
    fig.update_layout(title_text="Import/Export (GWh) sur la période 2018-2022", legend_title_text = "Légende :", width=800, height=400, template='simple_white')
    fig.update_xaxes(title_text='Temps en année')
    fig.update_yaxes(title_text="Import/Export (GWh)")
    fig.show()

    labels =["energy consumption non nucleiare","energy consumption nucleiare CVC-CJO", "energy consumption nucleiare CVS-CVC-CJO"]


    fig = go.Figure()
    i=0
    for column in consumption:
        fig.add_trace(go.Scatter(x=df_summaryze_electricity.Période, y=df_summaryze_electricity[column], name=labels[i]))
        i= i+1
    fig.update_layout(title_text="Consommation primaire d'énergie sur la période 2018-2022", legend_title_text = "Légende :", width=800, height=400, template='simple_white')
    fig.update_xaxes(title_text='Temps en année')
    fig.update_yaxes(title_text="Consommation primaire d'énergie (GWh)")
    fig.show()

        
if __name__ == "__main__":
    main()
