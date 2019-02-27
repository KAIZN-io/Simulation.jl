__author__ = 'Jan N. Piotraschke'
__email__ = 'jan.piotraschke@mail.de'
__version__ = 'bachelor_thesis'
__license__ = 'private'

from decimal import Decimal

import numpy as np
import pandas as pd
import itertools

from visualization import Visualizer
from values import SimulationTypes
from py_simulation.Solver import Solver


STUDYID = 'Yeast_BSc'
EXCAT = 'Salz'

class SimulationPreparation:
    def __init__(self, simulationData):
        self.simulationData = simulationData
        self.usedStimulusWithConcentration = None
        self.stimulusTimePoints = None

    def rulesForStimulus(self, stimulusDict={}, stimulusTimePoints={}):
        self.stimulusTimePoints = {}
        stimulusConcentrations = []
        stimulusNames = []

        """iterate over all available stimulus"""
        for key, values in stimulusDict.items():
            if values[-1] is True:
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
        modelAffectedFromStimulus,
        time_steps,
    ):
        """the 'universal' time list"""
        simulationTimePoints = [start, stop]

        # TEMP : bad way
        if self.simulationData['type'] in ['combined_models', 'ion']:
            simulationTimePoints.append(Glucose_impuls_start)

        runningChit = []

        for TRT, DOSE_list in self.usedStimulusWithConcentration.items():
            for singleDose in DOSE_list:
                """for every dose volume a new Simulation"""

                if modelAffectedFromStimulus == True:

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

                dict_runningChit = {'name': self.simulationData['type'],
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

                if modelAffectedFromStimulus == False:
                    break
            if modelAffectedFromStimulus == False:
                break
        if not runningChit:
            runningChit = [{
                'results': [np.arange(start, stop, time_steps)]
            }]
        return runningChit

def getOdeNames(initialValueSet):
    return [value['testcd'] for value in initialValueSet]

def isModelAffectedFromStimuli(odeNames, stimuli):
    for stimulus in stimuli:
        if set(stimulus['targets']).issubset(odeNames):
            return True

    return False

def getActiveStimuli(stimuli):
    return [stimulus for stimulus in stimuli if stimulus['active'] is True]

def getActiveImpulses(type, impulses):
    i = []
    for impulse in impulses:
        if impulse['substance'] is not 'NaCl' or type is SimulationTypes.hog:
            i.append(impulse)

    return i

def generate_dict_time(simulationData):
    d = {}

    for impulse in simulationData['impulses']:
        if impulse['substance'] == 'Glucose':
            d['Glucose_impuls_start'] =  impulse['start']
            d['Glucose_impuls_end']   =  impulse['stop']
        elif impulse['substance'] == 'NaCl':
            d['NaCl_impuls_start']     =  impulse['start']
            d['NaCl_impuls_firststop'] =  impulse['stop']

    return d

def generate_dict_uniqe_EXSTDTC(simulationData):
    dict_unique_EXSTDTC = {}

    for stimulus in simulationData['stimuli']:
        dict_unique_EXSTDTC[ stimulus['substance'] ] = stimulus['timings']

    return dict_unique_EXSTDTC

def generate_dict_stimulus(simulationData):
    dict_stimulus = {
        'NaCl_impuls' : [simulationData.get('nacl_impulse'), 'mM'],
        'signal_type' : [simulationData.get('signal_type')],
    }

    for stimulus in simulationData['stimuli']:
        dict_stimulus[ stimulus['substance'] ] = [
            [ stimulus['amount'] ],
            stimulus['unit'],
            stimulus['targets'],
            stimulus['active']
        ]

    return dict_stimulus

def simulate(simulationData):

    odeNames = getOdeNames(simulationData['initial_value_set'])
    type = SimulationTypes(simulationData['type'])
    stimuli = getActiveStimuli(simulationData['stimuli'])
    impulses = getActiveImpulses(type, simulationData['impulses'])
    modelAffectedFromStimuli = isModelAffectedFromStimuli(odeNames, stimuli)

    dict_time = generate_dict_time(simulationData)
    timeDict = {
        'Glucose_impuls_start': dict_time.get('Glucose_impuls_start') or 0,
        'Glucose_impuls_end': dict_time.get('Glucose_impuls_end') or 0,
        'NaCl_impuls_start': dict_time.get('NaCl_impuls_start') or 0,
        'NaCl_impuls_firststop': dict_time.get('NaCl_impuls_firststop') or 0,
    }
    uniqueEXSTDTC = generate_dict_uniqe_EXSTDTC(simulationData)
    stimulusDict = generate_dict_stimulus(simulationData)

    signal_type = stimulusDict.get('signal_type')[0] or 0
    NaCl_impuls = stimulusDict.get('NaCl_impuls')[0] or 0

    simulationPreparation = SimulationPreparation(simulationData)

    """"if the model is effected from the stimulus --> get the stimulus settings"""
    usedStimulusWithConcentration = simulationPreparation.rulesForStimulus(
        stimulusDict=stimulusDict,
        stimulusTimePoints=uniqueEXSTDTC
    )

    """time points for not external stimulated models"""
    runningChit = simulationPreparation.simulationTimePoints(
        start = simulationData['start'],
        stop = simulationData['stop'],
        time_steps = simulationData['step_size'],
        Glucose_impuls_start = timeDict['Glucose_impuls_start'],
        modelAffectedFromStimulus = modelAffectedFromStimuli,
    )

    """simulation

    the actual simulation begins
    """
    for simulationSettingsForTimeRange in runningChit:

        """initialize an empty DataFrame for each time value"""
        simulationFrame = pd.DataFrame()

        if modelAffectedFromStimuli:
            EXTRT = simulationSettingsForTimeRange['EXTRT']
            EXDOSE = simulationSettingsForTimeRange['EXDOSE']
            EXSTDTC = simulationSettingsForTimeRange['EXSTDTC']
        else:
            EXTRT = 0
            EXDOSE = 0
            EXSTDTC = [0]

        EX_dict = {
            "id": simulationData['id'],
            "uuid": simulationData['uuid'],
            "studyid": STUDYID,
            "domain": "ex",
            "usubjid": simulationData['type'],
            "excat": EXCAT,
            "extrt": EXTRT,
            "exdose": EXDOSE,
            "exdosu": "mM",
            "exstdtc_array": EXSTDTC,
            "simulation_start": simulationData['start'],
            "simulation_stop": simulationData['stop'],
            "co": "exstdtc in Sekunden",
            "pds": []
        }

        modelFingerprint = str(simulationData['id']) + '_' + simulationData['type']

        """initialValues creation"""
        initialValues = {}
        unitsForOdes = {}
        for value in simulationData['initial_value_set']:
            initialValues[value['testcd']] = value['orres']
            unitsForOdes[value['testcd']] = value['orresu']

        """DataFrame initialisieren"""
        simulationFrame = pd.DataFrame([initialValues], dtype='float')

        for i in simulationSettingsForTimeRange['results']:

            placeholderDataframe = []

            """ logic behind the simulation

            if the time has come ... and a stimulus is activated ...
            and a compartible model is choosen ...
            """

            if i[0] in EXSTDTC\
                    and modelAffectedFromStimuli == True:

                for TESTCDAffectedByStimulus in stimulusDict.get(EXTRT)[2]:
                    """adds the right value to the right ODE"""
                    simulationFrame.loc[i[0],
                                        TESTCDAffectedByStimulus] += EXDOSE

                """switch for glucose adding"""
                glucose_switch = [False]
            elif i[0] == timeDict['Glucose_impuls_start'] \
                    and modelAffectedFromStimuli == True:
                glucose_switch = [True]
            else:
                glucose_switch = [False]

            simulationFrame = Solver.callSimulation(
                simulationData = simulationData,
                Glucose_impuls_start = timeDict['Glucose_impuls_start'],
                Glucose_impuls_end = timeDict['Glucose_impuls_end'],
                NaCl_impuls_start = timeDict['NaCl_impuls_start'],
                NaCl_impuls_firststop = timeDict['NaCl_impuls_firststop'],
                glucose_switch = glucose_switch,
                signal_type = signal_type,
                NaCl_impuls = NaCl_impuls,
                dataForSimulation=simulationFrame,
                i=i
            )

        resultsForOdes, groupedPDORRESU = Visualizer.prepareVisualization(
            sql_USUBJID=simulationData['type'],
            ODE_RESULTS=simulationFrame,
            PDORRESU_x=unitsForOdes
        )

        """plot the results, save the plot and return the pictureName"""
        pictureName = Visualizer.plotTimeSeries(
            simulationData = simulationData,
            SEQ = simulationData['id'],
            timeSeriesData=resultsForOdes,
            subplotLogic=groupedPDORRESU
        )

        EX_dict['image_path'] = pictureName

        """last step before pushing results to database
        
        beautify the results
        """

        """round the time points"""
        roundByUsedTimeStepsgroupedPDORRESU = abs(
            Decimal(str(simulationData['step_size'])).as_tuple().exponent)

        oldTimeIndex = list(simulationFrame.index)
        newTimeIndex = np.round(oldTimeIndex, decimals=roundByUsedTimeStepsgroupedPDORRESU)

        dataframeAsMatrix = simulationFrame.values
        columnsOfDataframe = simulationFrame.columns.tolist()

        if not simulationData['type'] == 'volume':
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

        """get less data 
        
        only get each (1/time_steps) simulation results
        """
        simulationFrameFiltered = pd.DataFrame(
            dataframeAsMatrix,
            columns=columnsOfDataframe,
            index=newTimeIndex
        ) \
                .loc[::int(1/simulationData['step_size'])]

        dataframeAsDict = simulationFrameFiltered.to_dict('index')

        for DTC, innerDict in dataframeAsDict.items():
            for substance, value in innerDict.items():
                EX_dict['pds'].append({
                    'studyid' : STUDYID,
                    'domain' : 'pd',
                    'usubjid' : simulationData['type'],
                    'pdtestcd' : substance,
                    'pdtest' : None,
                    'pdorres' : value,
                    'pdorresu' : unitsForOdes[substance],
                    'pddtc' : DTC,
                    'co' : "pddtc in Sekunden",
                })

        return EX_dict

