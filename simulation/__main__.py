import os
import time
import pika
import time
import simplejson as json

import message_queue as mq
from SDTM import sdtm


QUEUE_SCHEDULED_SIMULATIONS = os.environ['QUEUE_SCHEDULED_SIMULATIONS']
QUEUE_SIMULATION_RESULTS    = os.environ['QUEUE_SIMULATION_RESULTS']
print(QUEUE_SIMULATION_RESULTS)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='task-queue'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_SCHEDULED_SIMULATIONS)
channel.queue_declare(queue=QUEUE_SIMULATION_RESULTS)

def processSimulation(ch, method, properties, body):
    simulationDict = json.loads(body, use_decimal=True)
    print('Simulation received, id: ' + str(simulationDict['id']))

    print('Simulating...')
    # result = sdtm(getArgsFromSimulationDict(simulation_data))
    time.sleep(5)

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
        if impulse.substance == 'Glucose':
            d['Glucose_impuls_start'] = str( impulse['start'] )
            d['Glucose_impuls_end']   = str( impulse['stop'] )
        elif impulse.substance == 'NaCl':
            d['NaCl_impuls_start']     = str( impulse['start'] )
            d['NaCl_impuls_firststop'] = str( impulse['stop'] )

    return d

def generate_dict_uniqe_EXSTDTC(simulationDict):
    dict_unique_EXSTDTC = {}

    for stimulus in simlationDict['stimuli']:
        dict_unique_EXSTDTC[ stimulus['substance'] ] = stimulus['timings']

    return dict_unique_EXSTDTC

def generate_dict_stimulus(simulationDict):
    dict_stimulus = {
        'NaCl_impuls' : [simulationDict['nacl_impulse'], 'mM'],
        'signal_type' : [simulationDict['signal_type']],
    }

    for stimulus in simlationDict['stimuli']:
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
            'specificInitValuesVersionSEQ': [self.initial_value_set.version],
            'specificModelVersionSEQ': [self.model.version],
            'specificParameterVersionSEQ': [self.parameter_set.version]
        }

    def generate_dicts(self):
        return {
            'dict_model_switch'   : generate_dict_model_switch(),
            'dict_time'           : generate_dict_time(),
            'dict_unique_EXSTDTC' : generate_dict_uniqe_EXSTDTC(),
            'dict_stimulus'       : generate_dict_stimulus(),
            'dict_system_switch'  : generate_dict_system_switch()
        }

channel.basic_qos(prefetch_count=1)
channel.basic_consume(processSimulation, queue=QUEUE_SCHEDULED_SIMULATIONS)

print("Waiting for simulations")
channel.start_consuming()

