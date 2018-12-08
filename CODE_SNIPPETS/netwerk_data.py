#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 13:39:10 2018

@author: janpiotraschke
"""


import tellurium as te
te.setDefaultPlottingEngine('matplotlib')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import preprocessing
import os
import tecombine
import urllib.request
import networkx as nx
import structural
import seaborn as sns
import sympy
from sklearn.gaussian_process import GaussianProcess


class netzwerk_daten_gewinnung:
    def __init__(self,loading_models=[],simlen = 1000,sim_points = 10000,
                 data_frames = [],corr_matrix=[], col=[]
                ,corr_for_each_parameter = [], development_of_parameter=[], development_of_time=[],
                model_counter = [],var=[],mean_for_parameter=[],CI_all=[],variance_all=[],time_for_fits=[]):
        self.loading_models=loading_models
        self.simlen=simlen
        self.sim_points=sim_points
        self.data_frames=data_frames
        self.corr_matrix=corr_matrix
        self.corr_for_each_parameter=corr_for_each_parameter
        self.development_of_parameter=development_of_parameter
        self.development_of_time=development_of_time
        self.model_counter=model_counter
        self.var=var
        self.mean_for_parameter=mean_for_parameter
        self.CI_all=CI_all
        self.variance_all=variance_all
        self.col=col
        self.time_for_fits=time_for_fits

    @property
    def load_model(self):

        #    #### Model aus dem Internet
        #    url = 'http://antimony.sourceforge.net/examples/biomodels/BIOMD0000000001.txt'
        #    request = urllib.request.Request(url)
        #    response = urllib.request.urlopen(request)
        #    bio2 = response.read().decode('utf-8')
        #    r_bio2 = te.loadAntimonyModel(bio2)

        #    print("Verwendbare Algorithmen: ",r.getAvailableIntegrators())
        #    print("Vorhandene Variabeln: ",r.getFloatingSpeciesIds())
        #    print("Vorhandene Parameter: ",r.getGlobalParameterIds())
        for i in self.loading_models:
            self.model_counter.append(te.loadSBMLModel(str(i)))

        #### wegen gillespie hat das eine Model iwie keine Parameterwerte
        for i in range(len(self.model_counter)):
            self.model_counter[i].setIntegrator('gillespie')
    #    print(self.model_counter[1].getFloatingSpeciesIds())

        return self.model_counter

    #@property
    def parameter_scan(self,parameter_range=[10],seeds=[1000],analyse_komponenten=[]):

        """
        Modelliert die in der Liste <<self.model_counter>> zwischengelagerte Modelle
        abhängig von einer Liste von Parameter-Werten für die ausgewählte
        Variable des Netzwerkes und abhängig von einer Liste von Seeds.

        Gibt eine Liste mit Panda DataFrame für die Korrelation von den zwei
        Modellen als Output raus.
        """
        simulation_results=[]
        corr_matrix_df=[]
        variable_hier=analyse_komponenten[1]
        # for i in analyse_komponenten:

        for parameter in parameter_range:
            # parameter_value=[]

            # listes=self.model_counter[1].getFloatingSpeciesIds()[3]
            # print(type(self.model_counter[1].Mdm2_mRNA))
            #print(type(float(self.model_counter[1].getFloatingSpeciesIds()[3])))


            # self.model_counter[1].Mdm2_mRNA=parameter
            # parameter_value.append(self.model_counter[1].Mdm2_mRNA)
            # print(parameter_value)

            """
            Simulationen, initialisiert mit dem selben seed, werden die gleichen
            Ergebnisse haben.
            """
            for i in seeds:
                for j in range(2):
                    self.model_counter[j].resetToOrigin()

                """
                Setzt die Variable auf den entsprechenden Wert.
                """
                self.model_counter[1][variable_hier]=parameter
                # finde den Variablennamen im jeweiligen Modell und ersetzte ihn durch einen String

                seed_value = i
                results = []
                #col = []
                ergebnislist=[]

                """
                Simuliert die Modelle.
                """
                for i in self.model_counter:
                    i.setSeed(seed_value)

                    i.integrator.variable_step_size = False
                    results.append(i.simulate(0,self.simlen,self.sim_points+1))

                """
                Erschafft Panda DataFrames mit den simulierten Werten der Modelle und
                gibt den DataFrame die für das Model entsprechende Species-Namen
                als Column.
                """
                for i in self.model_counter:
                    col_raw=['time']
                    for j in i.getFloatingSpeciesIds():
                        col_raw.append(j)
                    self.col.append(col_raw)
                dff = pd.DataFrame(results[0],columns=self.col[0])
                dfff = pd.DataFrame(results[1],columns=self.col[1])

                """
                Die untersuchte Variable steht in der nächsten Zeile in der Klammer.
                """
                self.development_of_parameter.append(dfff[analyse_komponenten[1]].tolist())
                self.development_of_time.append(dfff['time'].tolist())

                simulation_results.append([dff,dfff])
        return simulation_results

    def data_sorting(self, simulation_results=[]):

        """Sortiert die Daten nach ihren Parametern und übergibt sie jeweils der
        entsprechenden Liste"""

        data_sorted=[]
        iter_size = len(seeds)

        for i in range(0,len(simulation_results),iter_size):
            data_sorted.append(simulation_results[i:iter_size+i])

        # für Fehlersuche:
        # for i in range(len(parameter_range)):
        #     print(len(data_sorted[i]))

        return data_sorted

    def scheinkorrelation_results(self,data_sorted=[],to_excel=False,scheinkorrelation=False):

        """
        Berechnet jetzt die Korrelation zwischen den zwei Modellen.
        """
        """Anmerkung: Besitzen die Variablen die selbe Einheit? Pearson misst nur
        lineare Verhältnisse. Wenn Person ca. 0 beträgt, kann trotzdem noch
        Korrelation vorherschen, nämlich Nichtlineare. Spearman wäre dafür ein
        guter Ansatz. Sonst schaut man sich mal den scatter plot der beiden
        Variablen an."""

        corr_matrix=[]
        for i in data_sorted:
            corr_matrix_df=[]

            for j in i:
                ergebnislist=[]

                """hier ist er jetzt in der Liste, die die jeweiligen Simulationsergebnisse
                for seed und Parameter beinhalten"""
                for x in j[0]:
                    probelist=[]
                    for y in j[1]:
                #        print(y)
                        probelist.append(j[0][x].corr(j[1][y],method='pearson'))

                    ergebnislist.append(probelist)
                corr_matrix_df.append(pd.DataFrame(ergebnislist,columns=self.col[1],index=self.col[0]))
            corr_matrix.append(corr_matrix_df)
        ##### hier muss ich jetzt noch die entsprechenden DataFrame für jeden Parameter mit ihren Corr addieren.

        """ Berechnung Mittelwert der Korrelationen für jeden Parameterwert"""
        empty=[]
        for i in corr_matrix:
            mean_of_matrix=[]
            for j in i:
                if not mean_of_matrix:
                    mean_of_matrix.append(j)
                else:
                    mean_of_matrix[0]=mean_of_matrix[0]+j

            empty.append(mean_of_matrix[-1]/len(i))

        """ Die Zeit-Korrelation wird nun rausgenommen"""
        for i in range(len(empty)):
            if empty[i].at['time','time'] <1:
                print("Im Programm ist ein Fehler, da die Zeiten nicht korrelieren.")

            empty[i]=empty[i].drop('time',axis=1)
            empty[i]=empty[i].drop('time')

        # print("Minimum Wert: ",empty[0].min().min())
        # print("Maximum Wert: ",empty[0].max().max())

        """Sucht im jeweiligen DataFrame die Logalization raus, für die die Werte größer 0.9 sind """
        high_correlation=[]
        low_correlation=[]

        for i in empty:
            low_correlation.append([(i.index[x], i.columns[y]) for x,y in np.argwhere(abs(i.values) > 0)])

            #low_correlation.append([[i.index[x], i.columns[y]] for x,y in np.argwhere(i.values < 0)])


        """ruft die Werte für Corr(x,y) ab"""
        values_corr=[]
        for j in low_correlation:
            values_corr_per_parameter=[]
            for i in j:
                values_corr_per_parameter.append(empty[0].get_value(index=i[0],col=i[1]))
            values_corr.append(values_corr_per_parameter)

        correlation_indexes=[]
        for i in low_correlation:
            correlation_index=[]
            for j in i:
                correlation_index.append("Corr({},{})".format(j[0],j[1]))
            correlation_indexes.append(correlation_index)


        """erstellt das DataFrame für die Scheinkorrelation"""
        df_scheinkorrelation_list=[]
        for i in range(len(parameter_range)):
            df_scheinkorrelation_list.append(pd.DataFrame({parameter_range[i]:values_corr[i]},index=correlation_indexes[i]))

        """vereineint die DataFrame zu Einem"""
        df_scheinkorrelation=pd.DataFrame(df_scheinkorrelation_list[0])
        for i in range(1,len(parameter_range)):
            df_scheinkorrelation=pd.merge(df_scheinkorrelation,df_scheinkorrelation_list[i],
                                        left_index=True, right_index=True,how='outer')
        #print(df_scheinkorrelation)


        # """
        # Varianzrechnung der Korrelation.
        # """
        # for i in self.corr_for_each_parameter:
        #     """<<pd.concat>> verkettet die Panda DataFrames."""
        #     dff=pd.concat(i)
        #     #### .var(degreeoffreedom) degreeoffreedom kann man noch festlegen
        #     self.var = dff.groupby(level=0).var()
        #     empty.append(self.var)

        if to_excel is True:
            writer = pd.ExcelWriter('parameter.xlsx', engine='xlsxwriter')
            df_scheinkorrelation.to_excel(writer, sheet_name='report')
            writer.save()

        return df_scheinkorrelation #empty

    def korrelation_results(self,corr=[]):
        # corr ist ein DataFrame
        # Filter für Corr(X,Y) Auswahl

        # x=corr.sum(axis=1)/len(parameter_range)
        # kandidaten=[]
        # kandidaten.append(x.idxmin(axis=0))
        # print(kandidaten)
        # es wurde der falsche niedrigste Wert rausgefiltet. Keine Ahnung warum.
        # Damit wird aber erstmal exemplarisch weitergearbeitet.
        pass







####### fitten und visualisieren erst machen, wenn höchste Corr(x,y) und deren Matrix erstellt wurde
    def fit_on_values(self,data_sorted=[]):
        """Konfidenzintervall für die Fits kalkulieren"""
        """
        Sortiert die simulierten Werte nach Variablenwerteinstellung.
        Splittet die Liste in Untereinheiten, wo jeder Variablenwert für alle seine Seeds
        jeweils eine Unterheit für sich allein hat.
        """

        a=[]
        iter_size = len(seeds)

        for i in range(0,len(self.development_of_parameter),iter_size):
            a.append(self.development_of_parameter[i:iter_size+i])

        self.CI_all=[]
        for x in a:
            test_sum=[]
            tableData=x

            """Als erstes werden die simulierten Daten nach ihren Index sortiert"""
            for i in range(len(tableData[0])):
                test_values=[]
                for j in range(len(tableData)):
                    test_values.append(tableData[j][i])
                test_sum.append(test_values)
            mean_values = np.mean(test_sum, axis=1)


            """
            Varianz Berechnung. Code ist zwar sehr viel länger als np.var(), aber
            10 mal schneller dafür.
            """
            testy = list(zip(mean_values,test_sum))
            confidence_interval=[]
            square_difference=[]
            square_difference_sum=[]
            square_difference_same_index=[]

            for i,j in testy:
                square_difference=[]
                for k in j:
                    square_difference.append((k-i)**2)
                square_difference_same_index.append(square_difference)
            for i in square_difference_same_index:
                square_difference_sum.append(sum(i))

            n=len(seeds)
            variance=[]
            for i in square_difference_sum:
                variance.append(i/(n-1))

            """Berechnung des Konfidenzintervall. t-Faktor für 95,4 % Sicherheit"""
            ##### t-Wert sollte aus einem Dict entnommen werden, da er je nach n ausfällt.
            t=4.30
            CI=[]
            for i in variance:
                CI.append("{0:.2f}".format(t*np.sqrt(i/n)))

            self.variance_all.append(variance)
            self.CI_all.append(CI)

        self.mean_for_parameter=[list(np.mean(np.array(i),axis=0)) for i in a]

        for i in self.development_of_time[0:len(parameter_range)]:
            self.time_for_fits.append(list(np.array(i)))

    #@property
    def visualize(self,data=[],heat_map=False,plotting=False):
        """
        Visualisiert nach den Methoden, die True geschaltet sind. Benötigt eine
        Liste mit Panda DataFrame als Input.
        """
        if heat_map is True:
            plt.style.use('ggplot')
            cmap = sns.diverging_palette(220, 10, as_cmap=True)
            sns.heatmap(data, cmap=cmap,vmax=1,
                        square=True, linewidths=.5, cbar_kws={"shrink": .5})
            plt.savefig('picture/heat_map.png', dpi = 1200, format = 'png')
            plt.figure(figsize=(12,9))
            result = plt.show()


        elif plotting is True:
            for i,j in zip(self.development_of_time,self.development_of_parameter):
                plt.style.use('ggplot')
                plt.plot(i,j,color="grey",alpha=0.4)

                ax = plt.axes()
                ax.set_xlim()
                #ax.set_ylim(0,parameter_range[-1]+5)
                ax.set_xlabel("time[s]")
                ax.set_ylabel("concentration Mdm2_mRNA")
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.yaxis.grid(linewidth=0.5, color="black", alpha=0.3)
                # plt.legend(loc='best',fontsize=11)
                plt.tick_params(
                    which='both',
                    right='off',
                    top='off')

            """Mean plotten"""
            for i,j in zip(self.time_for_fits,self.mean_for_parameter):
                plt.plot(i,j,color="black")

            """Plottet Konfidenzintervall fablich"""
            for i in range(len(parameter_range)):
                upper_bound=[float(x)+float(y) for x, y in zip(self.mean_for_parameter[i],self.CI_all[i])]
                bottom_bound=[float(x)-float(y) for x, y in zip(self.mean_for_parameter[i],self.CI_all[i])]
                ax.fill_between(self.development_of_time[i],bottom_bound,upper_bound,alpha=0.2,label="Konfidenzintervall")

            plt.legend(loc='best',fontsize=8)
            plt.savefig('picture/Reporterplot.png', dpi = 1200, format = 'png')
            plt.figure(figsize=(12,9))
            result = plt.show()

        else:
            result = print("Nothing to visualize")
        return result


if __name__ == "__main__":

    seeds=list(range(1000,2010,500))
    parameter_range=list(range(10,21,10))

    loading_models = ["MyModels/BIOMD0000000001.xml","MyModels/BIOMD0000000188.xml"]
    x=netzwerk_daten_gewinnung(loading_models)
    x.load_model

    simulation_results = x.parameter_scan(parameter_range,seeds,analyse_komponenten=[0,'p53syn'])
    data_sorted = x.data_sorting(simulation_results)
    corr = x.scheinkorrelation_results(data_sorted=data_sorted,to_excel=False,scheinkorrelation=False)

    y=corr.sum(axis=1)/len(parameter_range)
    kandidaten_roh=[]
    kandidaten_roh.append(y.idxmin(axis=0))

    kandidaten=[]
    for i in range(len(kandidaten_roh)):
        kandidaten_einzeln=[]
        kandidaten_einzeln.append(kandidaten_roh[i][kandidaten_roh[i].find("(")+1:kandidaten_roh[i].find(",")])
        kandidaten_einzeln.append(kandidaten_roh[i][kandidaten_roh[i].find(",")+1:kandidaten_roh[i].find(")")])
        kandidaten.append(kandidaten_einzeln)

    print(kandidaten[0][1])



    #corr_fein=x.korrelation_results(corr=corr)
    x.fit_on_values(data_sorted=data_sorted)

    x.visualize(data=corr,plotting=True)
