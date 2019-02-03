import os
import time
import pika
import datetime
import simplejson as json

import message_queue as mq
from SDTM import sdtm
from db import sessionScope, Ex


QUEUE_SCHEDULED_SIMULATIONS = os.environ['QUEUE_SCHEDULED_SIMULATIONS']
QUEUE_SIMULATION_RESULTS    = os.environ['QUEUE_SIMULATION_RESULTS']

def processSimulation(ch, method, properties, body):
    simulationDict = json.loads(body, use_decimal=True)
    print('Simulation received, id: ' + str(simulationDict['id']))

    print('Simulating...')
    with sessionScope() as session:
        simulation = session.query(Ex) \
                .filter(Ex.id == simulationDict['id']) \
                .one()

        simulation.started_at = datetime.datetime.utcnow()

        result = sdtm(generate_dicts(simulationDict), simulation)

        simulation.finished_at = datetime.datetime.utcnow()


    print('Publishing results...')
    mq.publishSimulationResult({
        'simulation_id': simulationDict['id'],
        'pds': []
    })

    # confirm that the message was received and processed
    print('Acknoledgin that the simulation was received and processed...')
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print('Done')

def generate_dict_model_switch(simulationDict):
    return {
        'combined_models' : simulationDict['type'] == 'combined_models',
        'hog'             : simulationDict['type'] == 'hog',
        'ion'             : simulationDict['type'] == 'ion',
        'volume'          : simulationDict['type'] == 'volume',
    }

def generate_dict_time(simulationDict):
    d = {
        'start'      : simulationDict['start'],
        'stop'       : simulationDict['stop'],
        'time_steps' : str(simulationDict['step_size']),
    }

    for impulse in simulationDict['impulses']:
        if impulse['substance'] == 'Glucose':
            d['Glucose_impuls_start'] = str( impulse['start'] )
            d['Glucose_impuls_end']   = str( impulse['stop'] )
        elif impulse['substance'] == 'NaCl':
            d['NaCl_impuls_start']     = str( impulse['start'] )
            d['NaCl_impuls_firststop'] = str( impulse['stop'] )

    return d

def generate_dict_uniqe_EXSTDTC(simulationDict):
    dict_unique_EXSTDTC = {}

    for stimulus in simulationDict['stimuli']:
        dict_unique_EXSTDTC[ stimulus['substance'] ] = stimulus['timings']

    return dict_unique_EXSTDTC

def generate_dict_stimulus(simulationDict):
    dict_stimulus = {
        'NaCl_impuls' : [simulationDict.get('nacl_impulse'), 'mM'],
        'signal_type' : [simulationDict.get('signal_type')],
    }

    for stimulus in simulationDict['stimuli']:
        dict_stimulus[ stimulus['substance'] ] = [
            [ stimulus['amount'] ],
            stimulus['unit'],
            stimulus['targets'],
            stimulus['active']
        ]

    return dict_stimulus

def generate_dict_system_switch(simulationDict):
    return {
        'export_data_to_sql': True,
        'export_terms_data_to_sql': False,
        'specificInitValuesVersionSEQ': [1],
        'specificModelVersionSEQ': [1],
        'specificParameterVersionSEQ': [1]
    }

def generate_dicts(simulationDict):
    return {
        'uuid' : simulationDict['uuid'],
        'dict_model_switch'   : generate_dict_model_switch(simulationDict),
        'dict_time'           : generate_dict_time(simulationDict),
        'dict_unique_EXSTDTC' : generate_dict_uniqe_EXSTDTC(simulationDict),
        'dict_stimulus'       : generate_dict_stimulus(simulationDict),
        'dict_system_switch'  : generate_dict_system_switch(simulationDict)
    }

print("Waiting for simulations")
mq.listen(processSimulation, QUEUE_SCHEDULED_SIMULATIONS)

