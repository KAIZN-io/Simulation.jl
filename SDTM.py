__author__ = 'Jan N. Piotraschke'
__email__ = 'jan.piotraschke@mail.de'
__version__ = 'bachelor_thesis'
__license__ = 'private'

import sys
import logging
import uuid
from decimal import Decimal
from sqlalchemy import func

from db import Ex, Pd, ParameterSet, Parameter, InitialValueSet, InitialValue, sessionScope
from values import SimulationTypes
from DataExtraction import DataExtraction

"""import the standard used packages"""
exec(open("SYSTEM/py_packages.py").read())


logger = logging.getLogger(__name__)

# TODO: this class should be removed from SDTM.py
class DataVisualization:
    def __init__(self):
        pass

    def plotTimeSeries(
        simulation,
        SEQ,
        timeSeriesData=pd.DataFrame(),
        subplotLogic={},
        terms=False
    ):
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
        fig.suptitle(t='{}_Model'.format(simulation.getTypeAsString().title()),
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

                        if simulation.isOfType('combined_models') and i == 'Hog1PPn':
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

            pictureName = '{0}_{1}.png'.format(simulation.getTypeAsString(), SEQ)
            plt.savefig('SimulationPictures/{0}'.format(pictureName),
                        dpi=360,
                        format='png',
                        bbox_inches='tight'
                        )

            # """pre check if picture is already saved in database"""
            # cur.execute(sql.SQL("""
            #         Select max(seq) from {0}.analysis
            #         """).format(sql.Identifier(model.getName())))

            # if cur.fetchone()[0] != SEQ:
            #     cur.execute(sql.SQL("""
            #             INSERT INTO {0}.analysis(
            #                 seq, namepicture)
            #                 VALUES(%s, %s);
            #             """).format(sql.Identifier(model.getName())), [SEQ, pictureName])

            #     conn.commit()

            return pictureName

    def prepareVisualization(
        dict_visualisation,
        sql_USUBJID='',
        ODE_RESULTS=pd.DataFrame(),
        PDORRESU_x={}
    ):
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

class SimulationPreparation:
    def __init__(self, simulation):
        self.simulation = simulation
        self.usedStimulusWithConcentration = None
        self.stimulusTimePoints = None

    def isModelAffected(self, stimulusDict, activatedStimulus=[]):
        affectedModelFromStimulus = False

        """iterating over all activated stimuli"""
        for i in activatedStimulus:

            """get me the target of the specific stimuli"""
            target = stimulusDict.get(i)[2]

            """if the targets are in the specific model"""
            if set(target).issubset(self.simulation.getOdeNames()) == True:
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

    def simulationTimePoints(
        self,
        start,
        stop,
        Glucose_impuls_start,
        affectedModelFromStimulus,
        time_steps,
    ):
        """the 'universal' time list"""
        simulationTimePoints = [start, stop]

        # TEMP : bad way
        if self.simulation.isAnyOf(['combined_models', 'ion']):
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

                dict_runningChit = {'name': self.simulation.getTypeAsString(),
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

def sdtm(args, simulation):
    logger.debug(args)

    dict_visualisation = {
        'not_to_visualize': ['Yt', 'z1', 'z2', 'z3', 'z4', 'L_ArH', 'L_HH',
                             'Na_in', 'Na_out', 'K_out', 'K_in',
                             'Cl_out', 'H_in', 'H_out', 'ATP', 'Hog1PPc',
                             'Hog1c', 'Hog1n', 'Pbs2', 'Pbs2PP', 'R_ref', 'r_os', 'r_b', 'c_i', 'Sorbitol_out'],
    }

    STUDYID = 'Yeast_BSc'
    EXCAT = 'Salz'

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

    """activated stimuli

    find out which stimulus pipeline is opened for the experiment series
    """
    activated_stimuli = [stimulus_name for stimulus_name, items
                         in stimulusDict.items() if items[-1] == True]

    simulationPreparation = SimulationPreparation(simulation)

    """find out how and if the model is affected from the activated stimulus"""
    affectedModelFromStimulus = simulationPreparation.isModelAffected(
        stimulusDict = stimulusDict,
        activatedStimulus=activated_stimuli,
    )

    """"if the model is effected from the stimulus --> get the stimulus settings"""
    usedStimulusWithConcentration = simulationPreparation.rulesForStimulus(
        stimulusDict=stimulusDict,
        stimulusTimePoints=uniqueEXSTDTC
    )

    """time points for not external stimulated models"""
    runningChit = simulationPreparation.simulationTimePoints(
        start = timeDict['start'],
        stop = timeDict['stop'],
        Glucose_impuls_start = timeDict['Glucose_impuls_start'],
        affectedModelFromStimulus = affectedModelFromStimulus,
        time_steps = timeDict['time_steps'],
    )

    """simulation

    the actual simulation begins
    """
    logger.info('Simulation Type: ' + simulation.getTypeAsString())
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
            "uuid": args['uuid'],
            "studyid": STUDYID,
            "domain": "ex",
            "usubjid": simulation.getTypeAsString(),
            "excat": EXCAT,
            "extrt": EXTRT,
            "exdose": EXDOSE,
            "exdosu": "mM",
            "exstdtc_array": EXSTDTC,
            "simulation_start": timeDict['start'],
            "simulation_stop": timeDict['stop'],
            "co": "exstdtc in Sekunden",
        }
        simulation.extrt = EXTRT
        simulation.exdose = EXDOSE
        simulation.exstdtc_array = EXSTDTC

        modelFingerprint = str(SEQ) + '_' + simulation.getTypeAsString()

        """get the parameter from the database"""
        with sessionScope() as session:
            q = session.query(Parameter.testcd, Parameter.orres) \
                    .join(ParameterSet) \
                    .filter(ParameterSet.id == simulation.parameter_set_id)

        TESTCD_ORRESU_tuple = q.all()

        """initialValues creation"""
        parameterAsLocalVariables = {}
        for i in TESTCD_ORRESU_tuple:
            parameterAsLocalVariables[i[0]] = i[1]

        """make the dict keys as new variables"""
        locals().update(parameterAsLocalVariables)

        with sessionScope() as session:
            q = session.query(InitialValue.testcd, InitialValue.orres, InitialValue.orresu) \
                    .join(InitialValueSet) \
                    .filter(InitialValueSet.id == simulation.initial_value_set_id)

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
            elif i[0] == timeDict['Glucose_impuls_start'] \
                    and affectedModelFromStimulus == True:
                glucose_switch = [True]
            else:
                glucose_switch = [False]

            simulationFrame = DataExtraction.callSimulation(
                nameOfModel = simulation.getTypeAsString(),
                Glucose_impuls_start = timeDict['Glucose_impuls_start'],
                Glucose_impuls_end = timeDict['Glucose_impuls_end'],
                glucose_switch = glucose_switch,
                systemSwitchDict = systemSwitchDict,
                signal_type = signal_type,
                NaCl_impuls = NaCl_impuls,
                NaCl_impuls_start = timeDict['NaCl_impuls_start'],
                NaCl_impuls_firststop = timeDict['NaCl_impuls_firststop'],
                dataForSimulation=simulationFrame,
                i=i
            )

        """replace the time array with the simulation results"""
        simulationSettingsForTimeRange['results'] = simulationFrame

        """create a copy for the design of the plot"""
        rawOdeResults = simulationSettingsForTimeRange['results']

        resultsForOdes, groupedPDORRESU = DataVisualization.prepareVisualization(
            dict_visualisation = dict_visualisation,
            sql_USUBJID=simulation.getTypeAsString(),
            ODE_RESULTS=rawOdeResults,
            PDORRESU_x=simulationSettingsForTimeRange['units']
        )

        """plot the results, save the plot and return the pictureName"""
        pictureName = DataVisualization.plotTimeSeries(
            simulation = simulation,
            SEQ = SEQ,
            timeSeriesData=resultsForOdes,
            subplotLogic=groupedPDORRESU
        )

        EX_dict['image_path'] = pictureName
        simulation.image_path = pictureName

        logger.info('Simulation id: ' + str(SEQ))

        """last step before pushing results to database
        
        beautify the results
        """

        """round the time points"""
        roundByUsedTimeStepsgroupedPDORRESU = abs(
            Decimal(str(timeDict['time_steps'])).as_tuple().exponent)

        oldTimeIndex = list(simulationSettingsForTimeRange['results'].index)
        newTimeIndex = np.round(oldTimeIndex, decimals=roundByUsedTimeStepsgroupedPDORRESU)

        dataframeAsMatrix = simulationSettingsForTimeRange['results'].values
        columnsOfDataframe = simulationSettingsForTimeRange['results'].columns.tolist()

        if not simulation.isOfType('volume'):
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
        simulationSettingsForTimeRange['results'] = simulationSettingsForTimeRange['results'].loc[::int(1/timeDict['time_steps'])]

        """export the EX dict to the database"""
        if systemSwitchDict.get('export_data_to_sql') == True:
            with sessionScope() as session:
                """make the dict keys as new variables"""
                locals().update(simulationSettingsForTimeRange)

                dataframeAsDict = simulationSettingsForTimeRange['results'].to_dict('index')

                for DTC, innerDict in dataframeAsDict.items():
                    for substance, value in innerDict.items():
                        simulation.pds.append(Pd(
                            studyid = STUDYID,
                            domain = 'pd',
                            usubjid = simulation.getTypeAsString(),
                            pdtestcd = substance,
                            pdtest = None,
                            pdorres = value,
                            pdorresu = simulationSettingsForTimeRange['units'][substance],
                            pddtc = DTC,
                            co = "pddtc in Sekunden",
                        ))

            logger.info("Simulation results stored in database")

