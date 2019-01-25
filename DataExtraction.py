

class DataExtraction:
    def __init__(self):
        pass

    def solveTheODEs(initialValues, t):

        resultsDictPlaceholder = {}
        resultsOfTheTerms = ()

        """get the Names of the ODEs"""
        columnNames = simulationFrame.columns.tolist()

        """assing the initial values to their ODEs"""
        for i in range(len(initialValues)):
            try:
                exec('{}={}'.format(columnNames[i], initialValues[i]))

            except:
                print(columnNames[i], initialValues[i], 'time:', t)

        """get the model system from the json file"""
        with open('Single_Models/json_files/{0}_system.json'.format(
                nameOfModel)) as jsonData:
            dataFromJson = json.load(jsonData)

        """activate the model system"""
        for typeOfEquation, modelSpecies in dataFromJson.items():
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
        if systemSwitchDict.get('export_data_to_sql') == True\
                and systemSwitchDict.get('export_terms_data_to_sql') == True:

            """sql connection"""
            engine = create_engine(
                'postgres://postgres:@db_postgres:5432/simulation_results')

            dictWithTerms = {}
            for i in resultsOfTheTerms:
                dictWithTerms[i] = eval(i)

            df = pd.DataFrame(dictWithTerms, index=[t])

            df.to_sql(modelFingerprint, con=engine, schema='{}_terms'.format(
                nameOfModel), if_exists='append')

        return odeResultsForSolver

    def callSimulation(dataForSimulation=pd.DataFrame(), i=[]):
        initialValues = dataForSimulation.tail(1).values.tolist()[0]

        """solves the ode and algebraic equations"""
        states = odeint(DataExtraction.solveTheODEs, initialValues, i)

        """ruft die entsprechenden Columns Namen auf"""
        columnNames = dataForSimulation.columns.values.tolist()

        """uebergibt dem placeholderDataframe die Ergebnisse der Berechnung"""
        placeholderDataframe = pd.DataFrame(states, columns=columnNames, index=i)

        """haengt das placeholderDataframe dem simulationFrame an"""
        simulationFrame = pd.concat([dataForSimulation, placeholderDataframe])

        return simulationFrame

