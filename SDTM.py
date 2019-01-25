__author__ = 'Jan N. Piotraschke'
__email__ = 'jan.piotraschke@mail.de'
__version__ = 'bachelor_thesis'
__license__ = 'private'

import sys
import uuid
from decimal import Decimal
from sqlalchemy import func

from db import Ex, Pd, Model, Parameters, InitialValues, sessionScope, Session
from initializeModel import initializeDb
from values import SimulationTypes
from DataExtraction import DataExtraction

"""import the standard used packages"""
exec(open("SYSTEM/py_packages.py").read())


# TODO: this class should be removed from SDTM.py
class DataVisualization:
    def __init__(self):
        pass

    def plotTimeSeries(timeSeriesData=pd.DataFrame(),
                       subplotLogic={},
                       terms=False):
        """ def description

        this function only needs the ODE results and the ORRESU_dict to
        visualise the time-series

        subplotLogic = {ylabel_str : correspondingSubstance_list}
        """

        if len(subplotLogic.keys()) == 0:
            subplotLogic[1] = 'a'
            generalizePlot = True
        else:
            generalizePlot = False

        sns.set_style(style='whitegrid')
        # context : dict, None, or one of {paper, notebook, talk, poster}
        sns.set_context(context='talk')
        fig = plt.figure(figsize=(10, 7.5))

        """fontSize 16 is a good size for the thesis"""
        fontSize = 16

        """create the subplots"""
        iterNum = 1

        """pre define the subplots structures"""
        for ORRESU, j in subplotLogic.items():
            exec('ax{0} = fig.add_subplot({1}, 1, {0})'.format(iterNum,
                                                                len(subplotLogic)))
            exec('ax{}.spines["top"].set_visible(False)'.format(iterNum))
            exec(
                'ax{}.spines["right"].set_visible(False)'.format(iterNum))
            exec(
                'ax{}.set_xlabel("time [s]",fontsize=fontSize)'.format(iterNum))

            """fix the y-axis lim for pictures for latex / publication"""
            # exec('ax{}.set_ylim(bottom=-20000, top=50000)'.format(iterNum))

            if generalizePlot == True:
                exec("ax{}.set_ylabel('no unit',fontsize=fontSize)".format(iterNum))
            else:
                exec('ax{}.set_ylabel(ORRESU,fontsize=fontSize)'.format(iterNum))

            iterNum += 1

        """x axis is shared and the ticks are rotated"""
        fig.autofmt_xdate(bottom=0.2,
                            rotation=30)
        fig.suptitle(t='{}_Model'.format(nameOfModel.title()),
                        fontsize=fontSize)

        # fig.suptitle(t='Volume',
        #             fontsize=fontSize)

        with sns.color_palette('cubehelix', len(timeSeriesData.columns.tolist())):

            """make the fig more fittet"""
            # fig.tight_layout(pad = 3,
            #                 rect = [0,0,0.85,1]
            #                 )

            # """show the version of the plot"""
            # fig.text(0.99, 0.01,
            #          s='{} - {}'.format(current_date,
            #                             sql_USUBJID.title()),
            #          fontstyle='italic',
            #          color='#999999',
            #          ha='right',
            #          va='bottom',
            #          fontsize='x-small'
            #         )

            """assign each TESTCD to their right subplot"""
            if generalizePlot == False:
                for ORRESU_tuple, axis_index in zip(subplotLogic.items(),
                                                    range(1, len(subplotLogic)+1)):
                    parameter, substance = ORRESU_tuple

                    for i in substance:

                        if nameOfModel == 'combined_models' and i == 'Hog1PPn':
                            exec(
                                "ax{}.plot(timeSeriesData[i],label='Hog1PPn (*1E7)')".format(axis_index))

                        else:
                            if terms == True:
                                exec("ax{0}.plot(timeSeriesData[i],label=EquationTerms_dict[i])".format(
                                    axis_index))

                            else:
                                exec('ax{0}.plot(timeSeriesData[i],label=i)'.format(
                                    axis_index))

                        exec('ax{0}.legend(ncol=1,borderaxespad = 0,bbox_to_anchor=(1.01, 0.5), \
                            frameon = True,loc={1!r},fontsize=fontSize)'.format(axis_index, 'center left'))

            else:
                plotLabels = timeSeriesData.columns.tolist()
                for i in plotLabels:
                    exec('ax1.plot(timeSeriesData[i],label=i)')
                    exec("ax1.legend(ncol=1,borderaxespad = 0,bbox_to_anchor=(1.01, 0.5), \
                                frameon = True,loc='center left',fontsize=fontSize)")

            """"save the plot"""

            pictureName = '{0}_{1}.png'.format(nameOfModel, SEQ)
            plt.savefig('SimulationPictures/{0}'.format(pictureName),
                        dpi=360,
                        format='png',
                        bbox_inches='tight'
                        )

            # """pre check if picture is already saved in database"""
            # cur.execute(sql.SQL("""
            #         Select max(seq) from {0}.analysis
            #         """).format(sql.Identifier(nameOfModel)))

            # if cur.fetchone()[0] != SEQ:
            #     cur.execute(sql.SQL("""
            #             INSERT INTO {0}.analysis(
            #                 seq, namepicture)
            #                 VALUES(%s, %s);
            #             """).format(sql.Identifier(nameOfModel)), [SEQ, pictureName])

            #     conn.commit()

            return pictureName

    def prepareVisualization(sql_USUBJID='', ODE_RESULTS=pd.DataFrame(), PDORRESU_x={}):
        """conversion r to V

        convert the radius to the volume unit for better understandung of the
        cell system
        """

        # TEMP: temporary solution; PDORRESU = PDORRESU_x because otherwise it
        # overwrites the simulationSettingsForTimeRange['units'] dict --> local/global variable problem?
        if sql_USUBJID == 'combined_models':
            NotToVisualize = dict_visualisation.get('not_to_visualize')
            columnsOfDataframe = ODE_RESULTS.columns.tolist()

            ColumnsToVisualize = list(
                set(columnsOfDataframe) - set(NotToVisualize))

            for i in NotToVisualize:
                ODE_RESULTS = ODE_RESULTS.drop(columns=[i])

            PDORRESU = {
                i: PDORRESU_x[i] for i in ColumnsToVisualize if i in PDORRESU_x}

            try:
                ODE_RESULTS['Hog1PPn'] = ODE_RESULTS['Hog1PPn'] * 1E7
                # ODE_RESULTS['Cl_in'] = ODE_RESULTS['Cl_in'] / 10
            except:
                pass
        else:
            PDORRESU = PDORRESU_x

        convert_r_to_V = ['r', 'r_os', 'r_b', 'R_ref']
        ODE_RESULTS_columns = ODE_RESULTS.columns.tolist()
        for column_name in ODE_RESULTS_columns:

            if column_name in convert_r_to_V:
                ODE_RESULTS[column_name] = (
                    4/3) * np.pi * ODE_RESULTS[column_name]**3

                """"rename the column name

                change the first letter to 'V' and append then the rest of the
                old word string to this
                """
                new_column_name = 'V' + column_name[1:]
                ODE_RESULTS.rename(columns={column_name: new_column_name},
                                   inplace=True
                                   )
                """adapt the PDORRESU dict to the new units"""
                if column_name in PDORRESU:
                    PDORRESU[new_column_name] = PDORRESU.pop(column_name)
                    PDORRESU[new_column_name] = 'fL'

        """group the keys by their units"""
        groupedPDORRESU = {}
        for key, value in sorted(PDORRESU.items()):
            groupedPDORRESU.setdefault(value, []).append(key)

        """some design condition for the bachelor plots"""
        if sql_USUBJID == 'volume':
            ODE_RESULTS = pd.DataFrame(ODE_RESULTS['V'])
            groupedPDORRESU = {'total volume [fL]': ['V']}

        return ODE_RESULTS, groupedPDORRESU

# NOTE : class will be replace with ORM wrapper
class ModelFromDatabase:
    def __init__(self, type):
        self.type = type
        self.specificModelVersionSEQ = None
        self.specificInitValuesVersionSEQ = None

    def getModelVersion(self, requestedModelVersion=[]):
        """gets the wanted ModelVersion"""
        if len(requestedModelVersion) > 0:
            self.specificModelVersionSEQ = requestedModelVersion[0]

        else:
            """get the MAX(seq) value from the database"""
            with sessionScope() as session:
                q = session.query(func.max(Model.version)) \
                        .filter(Model.type == self.type)

            if q.scalar():
                self.specificModelVersionSEQ = q.scalar()
            else:
                self.specificModelVersionSEQ = 1

        return self.specificModelVersionSEQ

    def getInitValuesVersion(self, requestedInitValueVersion=[]):
        """gets the wanted InitValuesVersion"""
        if len(requestedInitValueVersion) > 0:
            self.specificInitValuesVersionSEQ = requestedInitValueVersion[0]

        else:
            """get the MAX(seq) value from the database"""
            with sessionScope() as session:
                q = session.query(func.max(InitialValues.version)) \
                        .filter(InitialValues.type == self.type)

            self.specificInitValuesVersionSEQ = q.scalar()

        return self.specificInitValuesVersionSEQ

    def getParameterVersion(self, requestedParameterVersion=[]):
        """gets the wanted ParameterValuesVersion"""
        if len(requestedParameterVersion) > 0:
            specificParameterVersionSEQ = requestedParameterVersion[0]

        else:
            """get the MAX(seq) value from the database"""
            with sessionScope() as session:
                q = session.query(func.max(Parameters.version)) \
                        .filter(Parameters.type == self.type)

            specificParameterVersionSEQ = q.scalar()

        return specificParameterVersionSEQ

    def updateLocalJsonModel(self):
        """update the local safed json file for the model"""
        with sessionScope() as session:
            q = session.query(Model.json) \
                    .filter(Model.version == self.specificModelVersionSEQ) \
                    .filter(Model.type == self.type)

        with open('Single_Models/json_files/{0}_system.json'.format(self.type.value), "w") as f:
            f.write(q.one()[0])

    def getODENames(self):
        """list of the names of the ODE in the model"""
        with sessionScope() as session:
            q = session.query(InitialValues.testcd) \
                    .filter(InitialValues.version == specificInitValuesVersionSEQ) \
                    .filter(InitialValues.type == self.type)

        modelOdeVariables = q.all()
        modelOdeVariables = [x[0] for x in modelOdeVariables]

        return modelOdeVariables


class SimulationPreparation:
    def __init__(self, nameOfModel):
        self.nameOfModel = nameOfModel
        self.usedStimulusWithConcentration = None
        self.stimulusTimePoints = None

    def isModelAffected(self, activatedStimulus=[], modelOdeVariables=[]):
        affectedModelFromStimulus = False

        """iterating over all activated stimuli"""
        for i in activatedStimulus:

            """get me the target of the specific stimuli"""
            target = stimulusDict.get(i)[2]

            """if the targets are in the specific model"""
            if set(target).issubset(modelOdeVariables) == True:
                affectedModelFromStimulus = True

        return affectedModelFromStimulus

    def rulesForStimulus(self, stimulusDict={}, stimulusTimePoints={}):
        self.stimulusTimePoints = {}
        stimulusConcentrations = []
        stimulusNames = []

        """iterate over all available stimulus"""
        for key, values in stimulusDict.items():
            if values[-1] == True:
                """get the concentrations"""
                # TEMP: bad way, because this only allows one kind of concentrations
                stimulusConcentrations.append(values[0])

                """get the stimulus name"""
                stimulusNames.append(key)

                """get all the stimulus time points"""
                if key in stimulusTimePoints.keys():

                    self.stimulusTimePoints[key] = stimulusTimePoints[key]

        self.usedStimulusWithConcentration = dict(
            zip(stimulusNames, stimulusConcentrations))

        return self.usedStimulusWithConcentration

    def simulationTimePoints(self):
        """the 'universal' time list"""
        simulationTimePoints = [start, stop]

        # TEMP : bad way
        if self.nameOfModel in ['combined_models', 'ion']:
            simulationTimePoints.append(Glucose_impuls_start)

        runningChit = []

        for TRT, DOSE_list in self.usedStimulusWithConcentration.items():
            for singleDose in DOSE_list:
                """for every dose volume a new Simulation"""

                if affectedModelFromStimulus == True:

                    """all the time points for this stimulus"""
                    simulationTimePoints.extend(self.stimulusTimePoints[TRT])

                    """if there are multiple stimuli events at one time point"""
                    simulationTimePoints = list(set(simulationTimePoints))
                    simulationTimePoints.sort()

                    switchboard = [1, 1, 1, 1, 1]

                else:
                    switchboard = [1, 0, 0, 0, 1]

                simulationTimePointsMatrix = [np.linspace(i, j, (j-i)/time_steps)
                                            for i, j in zip(simulationTimePoints[0::], simulationTimePoints[1::])
                                            ]

                dict_runningChit = {'name': self.nameOfModel,
                                     'EXTRT': TRT,
                                     'EXDOSE': singleDose,
                                     'EXSTDTC': self.stimulusTimePoints[TRT],
                                     'results': simulationTimePointsMatrix,
                                     }

                liste_compress = list(itertools.compress(
                    dict_runningChit, switchboard))

                dict_runningChit = {
                    i: dict_runningChit[i] for i in liste_compress}

                """append to the rest of the toodo simulation"""
                runningChit.append(dict_runningChit)

                if affectedModelFromStimulus == False:
                    break
            if affectedModelFromStimulus == False:
                break
        return runningChit


class Simulation():
    def __init__(self):
        pass


if __name__ == "__main__":

    initializeDb()

    dict_visualisation = {

        'not_to_visualize': ['Yt', 'z1', 'z2', 'z3', 'z4', 'L_ArH', 'L_HH',
                             'Na_in', 'Na_out', 'K_out', 'K_in',
                             'Cl_out', 'H_in', 'H_out', 'ATP', 'Hog1PPc',
                             'Hog1c', 'Hog1n', 'Pbs2', 'Pbs2PP', 'R_ref', 'r_os', 'r_b', 'c_i', 'Sorbitol_out'],
    }

    """momentanes arbeitsverzeichnis = cwd"""
    cwd = os.getcwd()

    if not os.path.isdir('SimulationPictures'):
        os.mkdir('SimulationPictures')

    STUDYID = 'Yeast_BSc'
    EXCAT = 'Salz'

    json_args = sys.argv[1]
    args = json.loads(json_args)

    print(sys.argv)
    timeDict = {
        'start': float(args['dict_time']['start']),
        'stop': float(args['dict_time']['stop']),
        'time_steps': float(args['dict_time']['time_steps']),
        'Glucose_impuls_start': float(args['dict_time']['Glucose_impuls_start']),
        'Glucose_impuls_end': float(args['dict_time']['Glucose_impuls_end']),
        'NaCl_impuls_start': float(args['dict_time']['NaCl_impuls_start']),
        'NaCl_impuls_firststop': float(args['dict_time']['NaCl_impuls_firststop']),
    }
    # TODO: will be replaced with enum
    dict_model_switch = args['dict_model_switch']
    uniqueEXSTDTC = args['dict_unique_EXSTDTC']
    stimulusDict = args['dict_stimulus']
    systemSwitchDict = args['dict_system_switch']

    """make the dict keys as new variables"""
    locals().update(timeDict)

    signal_type = stimulusDict.get('signal_type')[0]
    NaCl_impuls = stimulusDict.get('NaCl_impuls')[0]

    """host name taken from docker-compose.yml"""
    conn = psycopg2.connect(
        host='db_postgres',
        user='postgres',
        dbname='simulation_results'
    )

    """open a cursor to perform database operations"""
    cur = conn.cursor()

    """get the used model name"""
    # TODO: will be replaced with enum
    nameOfModel = [i for i, j in dict_model_switch.items() if j == True][0]

    """get the model
    
    name of model, initial values for the ODEs, parameterization, model, 
    and names of the ODEs
    """
    modelFromDatabase = ModelFromDatabase(SimulationTypes(nameOfModel))

    specificModelVersionSEQ = modelFromDatabase.getModelVersion(
        systemSwitchDict.get('specificModelVersionSEQ'))

    specificInitValuesVersionSEQ = modelFromDatabase.getInitValuesVersion(
        systemSwitchDict.get('specificInitValuesVersionSEQ'))

    specificParameterVersionSEQ = modelFromDatabase.getParameterVersion(
        systemSwitchDict.get('specificParameterVersionSEQ'))

    modelFromDatabase.updateLocalJsonModel()

    """get the ODE Names"""
    modelOdeVariables = modelFromDatabase.getODENames()

    """activated stimuli

    find out which stimulus pipeline is opened for the experiment series
    """
    activated_stimuli = [stimulus_name for stimulus_name, items
                         in stimulusDict.items() if items[-1] == True]

    simulationPreparation = SimulationPreparation(nameOfModel)

    """find out how and if the model is affected from the activated stimulus"""
    affectedModelFromStimulus = simulationPreparation.isModelAffected(
        activatedStimulus=activated_stimuli, modelOdeVariables=modelOdeVariables)

    """"if the model is effected from the stimulus --> get the stimulus settings"""
    usedStimulusWithConcentration = simulationPreparation.rulesForStimulus(
        stimulusDict=stimulusDict, stimulusTimePoints=uniqueEXSTDTC)

    """time points for not external stimulated models"""
    runningChit = simulationPreparation.simulationTimePoints()

    """simulation

    the actual simulation begins
    """
    print(nameOfModel)
    for simulationSettingsForTimeRange in runningChit:

        """initialize an empty DataFrame for each time value"""
        simulationFrame = pd.DataFrame()

        with sessionScope() as session:
            q = session.query(func.max(Ex.id))

        if q.scalar():
            SEQ = q.scalar() + 1
        else:
            SEQ = 1

        if affectedModelFromStimulus == False:
            EXTRT = 0
            EXDOSE = 0
            EXSTDTC = [0]

        else:
            EXTRT = simulationSettingsForTimeRange['EXTRT']
            EXDOSE = simulationSettingsForTimeRange['EXDOSE']
            EXSTDTC = simulationSettingsForTimeRange['EXSTDTC']

        EX_dict = {
            "id": SEQ,
            "studyid": STUDYID,
            "domain": "ex",
            "usubjid": nameOfModel,
            "excat": EXCAT,
            "extrt": EXTRT,
            "exdose": EXDOSE,
            "exdosu": "mM",
            "exstdtc_array": EXSTDTC,
            "simulation_start": start,
            "simulation_stop": stop,
            "co": "exstdtc in Sekunden",
            "model_id": specificModelVersionSEQ,
            "initial_values_version": specificInitValuesVersionSEQ,
            "parameters_version": specificParameterVersionSEQ
        }

        modelFingerprint = str(SEQ) + '_' + nameOfModel

        """get the parameter from the database"""
        with sessionScope() as session:
            q = session.query(Parameters.testcd, Parameters.orres) \
                    .filter(Parameters.type == SimulationTypes(nameOfModel)) \
                    .filter(Parameters.version == specificParameterVersionSEQ)

        TESTCD_ORRESU_tuple = q.all()

        """initialValues creation"""
        parameterAsLocalVariables = {}
        for i in TESTCD_ORRESU_tuple:
            parameterAsLocalVariables[i[0]] = i[1]

        """make the dict keys as new variables"""
        locals().update(parameterAsLocalVariables)

        with sessionScope() as session:
            q = session.query(InitialValues.testcd, InitialValues.orres, InitialValues.orresu) \
                    .filter(InitialValues.type == SimulationTypes(nameOfModel)) \
                    .filter(InitialValues.version == specificInitValuesVersionSEQ)

        TESTCD_ORRESU_tuple = q.all()

        """initialValues creation"""
        initialValues = {}
        unitsForOdes = {}
        for i in TESTCD_ORRESU_tuple:
            initialValues[i[0]] = i[1]
            unitsForOdes[i[0]] = i[2]

        """DataFrame initialisieren"""

        simulationSettingsForTimeRange['units'] = unitsForOdes

        simulationFrame = pd.DataFrame([initialValues])

        for i in simulationSettingsForTimeRange['results']:

            placeholderDataframe = []

            """ logic behind the simulation

            if the time has come ... and a stimulus is activated ...
            and a compartible model is choosen ...
            """

            if i[0] in EXSTDTC\
                    and affectedModelFromStimulus == True:

                for TESTCDAffectedByStimulus in stimulusDict.get(EXTRT)[2]:
                    """adds the right value to the right ODE"""
                    simulationFrame.loc[i[0],
                                        TESTCDAffectedByStimulus] += EXDOSE

                """switch for glucose adding"""
                glucose_switch = [False]
            elif i[0] == Glucose_impuls_start\
                    and affectedModelFromStimulus == True:
                glucose_switch = [True]
            else:
                glucose_switch = [False]

            simulationFrame = DataExtraction.callSimulation(
                nameOfModel = nameOfModel,
                Glucose_impuls_start = Glucose_impuls_start,
                Glucose_impuls_end = Glucose_impuls_end,
                glucose_switch = glucose_switch,
                systemSwitchDict = systemSwitchDict,
                signal_type = signal_type,
                NaCl_impuls = NaCl_impuls,
                NaCl_impuls_start = NaCl_impuls_start,
                NaCl_impuls_firststop = NaCl_impuls_firststop,
                dataForSimulation=simulationFrame,
                i=i
            )

        """replace the time array with the simulation results"""
        simulationSettingsForTimeRange['results'] = simulationFrame

        """create a copy for the design of the plot"""
        rawOdeResults = simulationSettingsForTimeRange['results']

        resultsForOdes, groupedPDORRESU = DataVisualization.prepareVisualization(
            sql_USUBJID=nameOfModel, ODE_RESULTS=rawOdeResults, PDORRESU_x=simulationSettingsForTimeRange['units'])

        """plot the results, save the plot and return the pictureName"""
        pictureName = DataVisualization.plotTimeSeries(timeSeriesData=resultsForOdes,
                                                       subplotLogic=groupedPDORRESU)

        EX_dict['image_path'] = pictureName

        print(SEQ, "nameOfModel", nameOfModel)

        """last step before pushing results to database
        
        beautify the results
        """

        """round the time points"""
        roundByUsedTimeStepsgroupedPDORRESU = abs(
            Decimal(str(time_steps)).as_tuple().exponent)

        oldTimeIndex = list(simulationSettingsForTimeRange['results'].index)
        newTimeIndex = np.round(oldTimeIndex, decimals=roundByUsedTimeStepsgroupedPDORRESU)

        dataframeAsMatrix = simulationSettingsForTimeRange['results'].values
        columnsOfDataframe = simulationSettingsForTimeRange['results'].columns.tolist()

        if nameOfModel != 'volume':
            def truncate(n, decimals=0):
                multiplier = 10 ** decimals
                return int(n * multiplier) / multiplier

            ROUND_AFTER_DIGITS_COUND = 5
            numbersWithoutZero = list(range(1, 10))
            numbersWithoutZero = [str(x) for x in numbersWithoutZero]

            for (x, y), unroundedValue in np.ndenumerate(dataframeAsMatrix):

                getDecimalPointPosition = str(unroundedValue).find('.')
                for index, i in enumerate(str(unroundedValue)):
                    if i in numbersWithoutZero:
                        firstOccurenceOfNaturalNumber = index
                        if index > getDecimalPointPosition:
                            firstOccurenceOfNaturalNumber -= 1
                        break

                truncateIndex = firstOccurenceOfNaturalNumber + \
                    ROUND_AFTER_DIGITS_COUND - getDecimalPointPosition

                roundedValue = truncate(unroundedValue, decimals=truncateIndex)

                dataframeAsMatrix[x, y] = roundedValue

        simulationSettingsForTimeRange['results'] = pd.DataFrame(dataframeAsMatrix,
                                      columns=columnsOfDataframe,
                                      index=newTimeIndex)

        """get less data 
        
        only get each (1/time_steps) simulation results
        """
        simulationSettingsForTimeRange['results'] = simulationSettingsForTimeRange['results'].loc[::int(1/time_steps)]

        """export the EX dict to the database"""
        if systemSwitchDict.get('export_data_to_sql') == True:
            with sessionScope() as session:
                """dict to sql database"""
                ex = Ex(**EX_dict)
                session.add(ex)
                session.commit()

                """make the dict keys as new variables"""
                locals().update(simulationSettingsForTimeRange)

                dataframeAsDict = simulationSettingsForTimeRange['results'].to_dict('index')

                pds = []
                for DTC, innerDict in dataframeAsDict.items():
                    for substance, value in innerDict.items():
                        pds.append(Pd(
                            ex_id = ex.id,
                            studyid = STUDYID,
                            domain = 'pd',
                            usubjid = nameOfModel,
                            pdtestcd = substance,
                            pdtest = None,
                            pdorres = value,
                            pdorresu = simulationSettingsForTimeRange['units'][substance],
                            pddtc = DTC,
                            co = "pddtc in Sekunden",
                        ))
                session.bulk_save_objects(pds)

            print("Daten hochgeladen")

    print("simulation finished")

    cur.close()
    conn.close()
