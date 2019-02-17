import pandas as pd
import numpy as np
from scipy.integrate import odeint
from collections import OrderedDict
import json


class Solver:
    def __init__(self):
        pass

    def solveTheODEs(
        initialValues,
        t,
        dataForSimulation,
        simulationData,
        Glucose_impuls_start,
        Glucose_impuls_end,
        NaCl_impuls_start,
        NaCl_impuls_firststop,
        glucose_switch,
        signal_type,
        NaCl_impuls,
    ):

        resultsDictPlaceholder = {}
        resultsOfTheTerms = ()

        """make initial values and parameters locallly available"""
        for value in simulationData['initial_value_set']:
            exec('{} = {}'.format(value['testcd'], value['orres']))

        for value in simulationData['parameter_set']:
            exec('{} = {}'.format(value['testcd'], value['orres']))


        """get the Names of the ODEs"""
        columnNames = dataForSimulation.columns.tolist()

        """assing the initial values to their ODEs"""
        for i in range(len(initialValues)):
            try:
                exec('{}={}'.format(columnNames[i], initialValues[i]))

            except:
                print(columnNames[i], initialValues[i], 'time:', t)

        """activate the model system"""
        for typeOfEquation, modelSpecies in simulationData['model'].items():
            if typeOfEquation == 'copa':
                for copaName, copaTerm in modelSpecies.items():

                    exec('{}={}'.format(copaName, copaTerm))

            else:
                """iterate over the content for the species"""
                for speciesName, speciesContent in modelSpecies.items():
                    if 'condition' in speciesContent:

                        for patialTerm, term in speciesContent['component'].items():

                            """activate the term under its condition"""
                            exec('{}={} {}'.format(patialTerm, term,
                                                   speciesContent['condition']))

                            """add patialTerm to a set / list for database"""
                            resultsOfTheTerms = resultsOfTheTerms + \
                                (patialTerm,)

                    else:
                        for patialTerm, term in speciesContent['component'].items():

                            exec('{}={}'.format(patialTerm, term))
                            resultsOfTheTerms = resultsOfTheTerms + \
                                (patialTerm,)

                    """rejoin the terms to their equation"""
                    list_values = list(speciesContent['component'].keys())

                    """
                    prepare to calculate the sum of the terms of a substance
                    """
                    equationTermsSum = '+'.join(list_values)

                    keysPlaceholder = speciesName
                    exec('{}={}'.format(keysPlaceholder, equationTermsSum))

                    if typeOfEquation == 'ODE':
                        resultsDictPlaceholder[speciesName] = eval(speciesName)

        """sort the odeResultsForSolverPlaceholder

        this must be done because the json file is not sorted!
        """
        resultsDictPlaceholder = OrderedDict(
            sorted(resultsDictPlaceholder.items()))

        """ODE results for the next simulation step of the ODE solver"""
        odeResultsForSolver = [j for i, j in resultsDictPlaceholder.items()]

        """export the individuel terms to the database"""
        # if systemSwitchDict.get('export_data_to_sql') == True\
        #         and systemSwitchDict.get('export_terms_data_to_sql') == True:
 
        #     """sql connection"""
        #     engine = create_engine(
        #         'postgres://postgres:@db_postgres:5432/simulation_results')
 
        #     dictWithTerms = {}
        #     for i in resultsOfTheTerms:
        #         dictWithTerms[i] = eval(i)
 
        #     df = pd.DataFrame(dictWithTerms, index=[t])
 
        #     df.to_sql(modelFingerprint, con=engine, schema='{}_terms'.format(
        #         nameOfModel), if_exists='append')
 
        return odeResultsForSolver

    def callSimulation(
        simulationData,
        Glucose_impuls_start,
        Glucose_impuls_end,
        NaCl_impuls_start,
        NaCl_impuls_firststop,
        glucose_switch,
        signal_type,
        NaCl_impuls,
        dataForSimulation=pd.DataFrame(dtype='float'),
        i=[],
    ):

        """solves the ode and algebraic equations"""
        states = odeint(
            func = Solver.solveTheODEs,
            y0 = dataForSimulation.tail(1).values.tolist()[0],
            t = i,
            args = (
                dataForSimulation,
                simulationData,
                Glucose_impuls_start,
                Glucose_impuls_end,
                NaCl_impuls_start,
                NaCl_impuls_firststop,
                glucose_switch,
                signal_type,
                NaCl_impuls,
            )
        )

        """ruft die entsprechenden Columns Namen auf"""
        columnNames = dataForSimulation.columns.values.tolist()

        """uebergibt dem placeholderDataframe die Ergebnisse der Berechnung"""
        placeholderDataframe = pd.DataFrame(states, columns=columnNames, index=i)

        """haengt das placeholderDataframe dem simulationFrame an"""
        dataForSimulation = pd.concat([dataForSimulation, placeholderDataframe])

        return dataForSimulation

