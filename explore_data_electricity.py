#!/usr/bin/python

import os, sys
import pandas as pd
import matplotlib.pyplot as plt
# Open a file
path = os.getcwd()
dirs = os.listdir( path +'/Data/')

print(path)

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


    
    #print(df_price_menage_electricity.info())
    
    
    #print(df_price_industry_electricity.info())
    print(df_electricity_2023.info())
    #print(df_summaryze_electricity.columns.to_list())
    
    
    
    #print(df_summaryze_electricity.info())
    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------- price menage ------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------

    price_menage_electricity = df_price_menage_electricity.columns[1:].to_list()
    labels = ["toutes tranches","tranches DA", "tranches DB", "tranches DC","tranches DD","tranches DE"]
    plt.figure(figsize=(9, 12))
    i=0
    for column in price_menage_electricity:
        plt.plot(df_price_menage_electricity.Période,df_price_menage_electricity[column], label = labels[i])
        i= i+1
    plt.xlabel("Time(Months)")
    plt.ylabel("Prix au détail de l'électricité TTC (eur)")
    plt.legend()
    #plt.show()
    #----------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------- price industry ----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------
    price_industry_electricity = df_price_industry_electricity.columns[1:].to_list()
    labels = ["tranches IA à IF","tranches IA", "tranches IB", "tranches IC","tranches ID","tranches IE", "tranches IF","tranches IG","toutes tranches" ]
    plt.figure(figsize=(9, 12))
    i=0
    for column in price_industry_electricity:
        plt.plot(df_price_industry_electricity.Période,df_price_industry_electricity[column], label = labels[i])
        i= i+1
    plt.xlabel("Time(Months)")
    plt.ylabel("Prix au détail de l'électricité hors TVA (eur)")
    plt.legend()
    #plt.show()
    
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
    plt.figure(figsize=(9, 12))
    i=0
    labels = ["Production totale  d'électricité","électricité nucléaire", "électricité hydraulique", "électricité éolienne","électricité photovoltaïque","électricité thermique"]
    for column in production_brut:
        plt.plot(df_electricity_2023.Période,df_electricity_2023[column], label = labels[i])
        i= i+1
    plt.xlabel("Time(Months)")
    plt.ylabel("Production brute d'électricité (GWh)")
    plt.legend()

    plt.figure(figsize=(9, 12))
    i=0
    for column in production_net:
        plt.plot(df_electricity_2023.Période,df_electricity_2023[column], label = labels[i])
        i= i+1
    plt.xlabel("Time(Months)")
    plt.ylabel("Production nette d'électricité (GWh)")
    plt.legend()
    plt.show()


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

    plt.figure(figsize=(9, 12))
    labels =["total: hydraulic - eolic - solar electricity ","hydraulic electricity","eolic electricity","solar electricity","production nuclear"]
    i = 0
    for column in production:
        
        plt.plot(df_summaryze_electricity.Période,df_summaryze_electricity[column], label = labels[i])
        i= i+1
    plt.xlabel("Time(Months)")
    plt.ylabel("Production (GWh)")
    plt.legend()

    plt.figure(figsize=(9, 12))
    labels =["Total_import_export","import", "export"]
    i = 0
    for column in import_export:
        
        plt.plot(df_summaryze_electricity.Période,df_summaryze_electricity[column], label = labels[i])
        i= i+1
    plt.xlabel("Time(Months)")
    plt.ylabel("Import/Export (GWh)")
    plt.legend()

    plt.figure(figsize=(9, 12))
    labels =["energy consumption non nucleiare","energy consumption nucleiare CVC-CJO", "energy consumption nucleiare CVS-CVC-CJO"]
    i = 0
    for column in consumption:
        
        plt.plot(df_summaryze_electricity.Période,df_summaryze_electricity[column], label = labels[i])
        i= i+1
    plt.xlabel("Time(Months)")
    plt.ylabel("Compsumptions (GWh)")
    plt.legend()

    #plt.show()
        
if __name__ == "__main__":
    main()
