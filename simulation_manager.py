import json
import subprocess
import multiprocessing
import time
import datetime
import uuid
from sqlalchemy import func

from web_interface.simulation_form import simulation_models
from db import Ex, sessionScope


class SimulationManager:
    def __init__( self ):
        self.simulations = []

    def start_new_simulation(self, data):
        if not self.has_running_simulation():
            new_simulation = Simulation(
                seq = self.get_new_seq_number( data["model"] ),
                data = data
            )
            new_simulation.start()
            self.simulations.append(new_simulation)

    def get_running_simulations(self):
        return [sim for sim in self.simulations if sim.is_running()]

    def get_finished_simulations(self):
        return [sim for sim in self.simulations if not sim.is_running()]

    def has_running_simulation(self):
        return len(self.get_running_simulations()) > 0

    def get_new_seq_number(self, model):
        with sessionScope() as session:
            q = session.query(func.max(Ex.id))

        if q.scalar():
            return q.scalar()
        else:
            return 1

class SimulationProcess(multiprocessing.Process):
    def __init__(self, dicts):
        super(SimulationProcess, self).__init__()
        self.dicts = dicts

    def run(self):
        args = json.dumps(self.dicts)
        subprocess.call(["python", "-u", "SDTM.py", args])


class Simulation:
    def __init__(self, seq, data):
        self.name = data['name']
        self.uuid = uuid.uuid4()
        self.seq = seq
        self.data = get_simulation_data_from_form(data)
        self.created_at = datetime.datetime.now()
        self.started_at = None
        self.model = data['model']

        self.process = SimulationProcess(dicts=self.data.generate_dicts())

    def start(self):
        self.process.start()
        self.started_at = datetime.datetime.now()

    def is_running(self):
        return self.process.is_alive()

    def get_picture_name(self):
        return '%s_%d.png'%(self.model, self.seq)

class SimulationData:
    def __init__(self, name, model, start, stop, step_size, impulses, stimuli ):
        self.name = name
        self.model = model

        self.start = start
        self.stop = stop
        self.step_size = step_size

        self.impulses = impulses
        self.stimuli = stimuli

        self.uuid = uuid.uuid4()

    def get_model_name(self):
        return simulation_models[self.model]

    def generate_dict_model_switch(self):
        return {
            'combined_models' : self.model == 'combined_models',
            'hog'             : self.model == 'hog',
            'ion'             : self.model == 'ion',
            'volume'          : self.model == 'volume',
        }

    def generate_dict_time(self):
        return {
            'start'                 : self.start,
            'stop'                  : self.stop,
            'time_steps'            : str( self.step_size ),
            'Glucose_impuls_start'  : str( self.impulses['Glucose'].start ),
            'Glucose_impuls_end'    : str( self.impulses['Glucose'].stop ),
            'NaCl_impuls_start'     : str( self.impulses['NaCl'].start ),
            'NaCl_impuls_firststop' : str( self.impulses['NaCl'].stop ),
        }

    def generate_dict_uniqe_EXSTDTC(self):
        dict_unique_EXSTDTC = {}

        for stimulus in self.stimuli:
            dict_unique_EXSTDTC[ stimulus.substance ] = stimulus.timing

        return dict_unique_EXSTDTC

    def generate_dict_stimulus(self):
        dict_stimulus = {
            'NaCl_impuls' : [200, 'mM'],
            'signal_type' : [2],
        }

        for stimulus in self.stimuli:
            dict_stimulus[ stimulus.substance ] = stimulus.get_as_array()

        return dict_stimulus

    def generate_dict_system_switch(self):
        return {
            'export_data_to_sql': True,
            'export_terms_data_to_sql': False,
            'specificInitValuesVersionSEQ': [1],
            'specificModelVersionSEQ': [1],
            'specificParameterVersionSEQ': [1]
        }

    def generate_dicts(self):
        return {
            'dict_model_switch'   : self.generate_dict_model_switch(),
            'dict_time'           : self.generate_dict_time(),
            'dict_unique_EXSTDTC' : self.generate_dict_uniqe_EXSTDTC(),
            'dict_stimulus'       : self.generate_dict_stimulus(),
            'dict_system_switch'  : self.generate_dict_system_switch()
        }

class Impulse:
    def __init__(self, substance, start, stop):
        self.substance = substance
        self.start = start
        self.stop = stop

class Stimulus:
    def __init__(self, substance, amount, unit, target, timing, active):
        self.substance = substance
        self.amount = amount
        self.unit = unit
        self.target = target
        self.timing = timing
        self.active = active

    def get_as_array(self):
        return [ [ self.amount ], self.unit, self.target, self.active ]

def get_simulation_data_from_form(form_data):
    return SimulationData(
        name = form_data['name'],
        model = form_data['model'],

        start = form_data['start'],
        stop = form_data['stop'],
        step_size = form_data['step_size'],

        impulses = get_impulses_from_form_data(form_data),
        stimuli = get_stimuli_from_form_data(form_data)
    )

def get_impulses_from_form_data(form_data):
    return {
        'Glucose': Impulse(
            substance = 'Glucose',
            start = form_data['glucose_impulse_start'],
            stop = form_data['glucose_impulse_stop']
        ),
        'NaCl': Impulse(
            substance = 'NaCl',
            start = form_data['nacl_impulse_start'],
            stop = form_data['nacl_impulse_stop']
        )
    }

def get_stimuli_from_form_data(form_data):
    return [
        Stimulus(
            substance = 'KCl',
            amount = form_data['kcl_amount'],
            unit = 'mM',
            target = ['K_out', 'Cl_out'],
            timing = [ int( e ) for e in form_data['kcl_timing'].split(',') ],
            active = form_data['kcl_active']
        ),
        Stimulus(
            substance = 'NaCl',
            amount = form_data['nacl_amount'],
            unit = 'mM',
            target = ['Na_out', 'Cl_out'],
            timing = [ int( e ) for e in form_data['nacl_timing'].split(',') ],
            active = form_data['nacl_active']
        ),
        Stimulus(
            substance = 'Sorbitol',
            amount = form_data['sorbitol_amount'],
            unit = 'mM',
            target = ['Sorbitol_out'],
            timing = [ int( e ) for e in form_data['sorbitol_timing'].split(',') ],
            active = form_data['sorbitol_active']
        ),
    ]

