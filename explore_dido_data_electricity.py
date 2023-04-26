#!/usr/bin/python

import pandas as pd
import plotly.graph_objects as go
from module_read_plot_electricity_dido_data import dirs, read_electricity_data, plot_from_df, plot_from_df_with_list_col, plot_first_column_from_df1_df2
# Open a file

print(dirs)



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
