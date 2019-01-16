import multiprocessing
import time
import datetime
import uuid
import subprocess

class SimulationManager:
    def __init__( self ):
        self.simulations = []

    def start_new_simulation( self, data ):
        new_simulation = Simulation( data )
        new_simulation.start()
        self.simulations.append( new_simulation )

    def get_running_simulations( self ):
        return [ sim for sim in self.simulations if sim.is_running() ]

class SimulationProcess( multiprocessing.Process ):
    def __init__(self, dicts ):
        super( SimulationProcess, self ).__init__()
        self.dicts = dicts

    def run(self):
        """ermöglicht bash Befehle auszuführen"""
        p = subprocess.Popen(["python","SDTM.py"])
        o,e = p.communicate()

class Simulation:
    def __init__( self, data ):
        self.name = data['name']
        self.uuid = uuid.uuid4()
        self.data = data
        self.created_at = datetime.datetime.now()
        self.started_at = None
        self.dicts = {
            'dict_model_switch'   : get_dict_model_switch( data ),
            'dict_time'           : get_dict_time( data ),
            'dict_unique_EXSTDTC' : get_dict_uniqe_EXSTDTC( data ),
            'dict_stimulus'       : get_dict_stimulus( data ),
            'dict_system_switch'  : get_dict_system_switch( data )
        }

        self.process = SimulationProcess( dicts=self.dicts )

    def start( self ):
        self.process.start()
        self.started_at = datetime.datetime.now()

    def is_running( self ):
        return self.process.is_alive()

def get_dict_model_switch( data ):
    return {
        'combined_models' : data['model'] == 'combined_models',
        'hog'             : data['model'] == 'hog',
        'ion'             : data['model'] == 'ion',
        'volume'          : data['model'] == 'volume',
    }

def get_dict_time( data ):
    return {
        'start'                : data['start'],
        'stop'                 : data['stop'],
        'time_steps'           : data['step_size'],
        'Glucose_impuls_start' : data['glucose_impulse_start'],
        'Glucose_impuls_end'   : data['glucose_impulse_stop']
    }

def get_dict_uniqe_EXSTDTC( data ):
    return {
        'KCl' : [30,60,100],
        'NaCl' : [30],
        'Sorbitol' : [30],
    }

def get_dict_stimulus( data ):
    return {
        'KCl' : [[100], 'mM', ['K_out','Cl_out'], True],
        'NaCl': [[800], 'mM', ['Na_out', 'Cl_out'], False],
        'Sorbitol': [[1600], 'mM', ['Sorbitol_out'], False],
        'NaCl_impuls' : [200, 'mM'],
        'signal_type' : [2],
    }

def get_dict_system_switch( data ):
    return {
        'export_data_to_sql' : False,
        'export_terms_data_to_sql' : False,
        'SpecificInitValuesVersionSEQ' : [2],
        'SpecificModelVersionSEQ' : [14]
    }

