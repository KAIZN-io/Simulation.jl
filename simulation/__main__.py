import os
import simplejson as json
from datetime import datetime

import message_queue as mq
from SDTM import sdtm
from values import RFC3339_DATE_FORMAT


QUEUE_SCHEDULED_SIMULATIONS = os.environ['QUEUE_SCHEDULED_SIMULATIONS']
QUEUE_SIMULATION_RESULTS    = os.environ['QUEUE_SIMULATION_RESULTS']

def processSimulation(ch, method, properties, body):
    simulationData = json.loads(body, use_decimal=True)
    print('Simulation received, id: ' + str(simulationData['id']))

    print('Simulating...')
    started_at = datetime.utcnow()
    result = sdtm(generate_dicts(simulationData), simulationData)
    finished_at = datetime.utcnow()

    print('Publishing results...')
    mq.publishSimulationResult({
        'simulation_id': simulationData['id'],
        'started_at': started_at.strftime(RFC3339_DATE_FORMAT),
        'finished_at': finished_at.strftime(RFC3339_DATE_FORMAT),
        'extrt': result['extrt'],
        'exdose': result['exdose'],
        'exstdtc_array': result['exstdtc_array'],
        'image_path': result['image_path'],
        'pds': result['pds']
    })

    # confirm that the message was received and processed
    print('Acknowledging that the simulation was received and processed...')
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print('Done')

def generate_dict_model_switch(simulationData):
    return {
        'combined_models' : simulationData['type'] == 'combined_models',
        'hog'             : simulationData['type'] == 'hog',
        'ion'             : simulationData['type'] == 'ion',
        'volume'          : simulationData['type'] == 'volume',
    }

def generate_dict_time(simulationData):
    d = {
        'start'      : simulationData['start'],
        'stop'       : simulationData['stop'],
        'time_steps' : str(simulationData['step_size']),
    }

    for impulse in simulationData['impulses']:
        if impulse['substance'] == 'Glucose':
            d['Glucose_impuls_start'] = str( impulse['start'] )
            d['Glucose_impuls_end']   = str( impulse['stop'] )
        elif impulse['substance'] == 'NaCl':
            d['NaCl_impuls_start']     = str( impulse['start'] )
            d['NaCl_impuls_firststop'] = str( impulse['stop'] )

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

def generate_dict_system_switch(simulationData):
    return {
        'export_data_to_sql': True,
        'export_terms_data_to_sql': False,
        'specificInitValuesVersionSEQ': [1],
        'specificModelVersionSEQ': [1],
        'specificParameterVersionSEQ': [1]
    }

def generate_dicts(simulationData):
    return {
        'id'    : simulationData['id'],
        'uuid'  : simulationData['uuid'],
        'type'  : simulationData['type'],
        'model' : simulationData['model'],
        'dict_model_switch'   : generate_dict_model_switch(simulationData),
        'dict_time'           : generate_dict_time(simulationData),
        'dict_unique_EXSTDTC' : generate_dict_uniqe_EXSTDTC(simulationData),
        'dict_stimulus'       : generate_dict_stimulus(simulationData),
        'dict_system_switch'  : generate_dict_system_switch(simulationData)
    }

print("Waiting for simulations")
mq.listen(processSimulation, QUEUE_SCHEDULED_SIMULATIONS)

