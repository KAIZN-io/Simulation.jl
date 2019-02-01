import json
import logging
import subprocess
import multiprocessing
import time
import datetime
import uuid
from sqlalchemy import func

from web_interface.simulation_form import simulation_models
from db import Ex, Model, InitialValueSet, ParameterSet, Impulse, Stimulus, sessionScope, ThreadScopedSession
from values import SimulationTypes
from SDTM import sdtm


logger = logging.getLogger(__name__)

class SimulationManager:
    def __init__( self ):
        self.processes = []

    def start_new_simulation(self, formData):
        if not self.has_running_simulation():
            new_simulation = getSimulationFromFormData(formData)
            new_process = SimulationProcess(new_simulation)
            new_process.start()
            self.processes.append(new_process)

    def get_running_simulations(self):
        return [process.simulation for process in self.processes if process.is_running()]

    def get_finished_simulations(self):
        with sessionScope() as session:
            return session.query(Ex).filter(Ex.finished_at != None).all()

    def has_running_simulation(self):
        return len(self.get_running_simulations()) > 0

class SimulationProcess(multiprocessing.Process):
    def __init__(self, simulation):
        assert isinstance(simulation, Ex)

        super(SimulationProcess, self).__init__()

        self.simulation = simulation
        self.dicts = simulation.generate_dicts()
        self.uuid = self.simulation.uuid

    def start(self):
        # update the started at value
        self.simulation.started_at = datetime.datetime.now()

        super().start()

    def is_running(self):
        return self.is_alive()

    def get_simulation(self):
        return self.simulation

    def get_picture_name(self):
        return self.simulation.image_path

    def run(self):
        logger.info('Simulation process started')

        # get settion
        threadScopedSession = ThreadScopedSession()
        session = threadScopedSession()
        logger.debug('session id: ' + str(id(session)))

        # get the simulation so we are not working with a copy from the main thread
        # and possibly get into issues. This makes sure the session is bound to our
        # thread scoped session and not the session of the main thread.
        simulation = session.query(Ex).filter(Ex.id == self.simulation.id).one()

        # prepare args and call sdtm
        self.dicts['uuid'] = str(self.uuid)
        sdtm(self.dicts, simulation)

        # set the finished at time
        simulation.finished_at = datetime.datetime.now()

        # make sure to write the changes to the db
        session.commit()

        # cleaning up
        threadScopedSession.remove()

        logger.info('Simulation process ended')

def getSimulationFromFormData(formData):
    modelType = SimulationTypes(formData['model'])

    with sessionScope() as session:
        model = session.query(Model) \
                .filter(Model.type == modelType) \
                .filter(Model.version == 1) \
                .one()

        initialValueSet = session.query(InitialValueSet) \
                .filter(InitialValueSet.type == modelType) \
                .filter(InitialValueSet.version == 1) \
                .one()

        parameterSet = session.query(ParameterSet) \
                .filter(ParameterSet.type == modelType) \
                .filter(ParameterSet.version == 1) \
                .one()

        ex = Ex(
            name              = formData['name'],

            model_id             = model.id,
            model                = model,
            initial_value_set_id = initialValueSet.id,
            initial_value_set    = initialValueSet,
            parameter_set_id     = parameterSet.id,
            parameter_set        = parameterSet,

            hog_signal_type   = formData['hog_signal_type'],
            hog_nacl_impulse  = formData['hog_nacl_impulse'],

            studyid           = 'Yeast_BSc',
            usubjid           = modelType.name,
            excat             = 'Salz',
            domain            = "ex",
            exdosu            = "mM",
            start             = formData['start'],
            stop              = formData['stop'],
            step_size         = formData['step_size'],
            co                = "exstdtc in Sekunden",
        )

        session.add(ex)
        session.commit()

        ex.impulses.append(Impulse(
            substance = 'Glucose',
            start = formData['glucose_impulse_start'],
            stop = formData['glucose_impulse_stop']
        ))

        ex.impulses.append(Impulse(
            substance = 'NaCl',
            start = formData['nacl_impulse_start'],
            stop = formData['nacl_impulse_stop']
        ))

        kcl_stimulus = Stimulus(
            substance = 'KCl',
            amount = formData['kcl_amount'],
            unit = 'mM',
            targets = ['K_out', 'Cl_out'],
            timings = [ int( e ) for e in formData['kcl_timing'].split(',') ],
            active = formData['kcl_active']
        )
        # if formData['kcl_active'] and isStimulusAffectingSimulation(kcl_stimulus, ex):
        ex.stimuli.append(kcl_stimulus)

        nacl_stimulus = Stimulus(
            substance = 'NaCl',
            amount = formData['nacl_amount'],
            unit = 'mM',
            targets = ['Na_out', 'Cl_out'],
            timings = [ int( e ) for e in formData['nacl_timing'].split(',') ],
            active = formData['nacl_active']
        )
        # if formData['nacl_active'] and isStimulusAffectingSimulation(nacl_stimulus, ex):
        ex.stimuli.append(nacl_stimulus)

        sorbitol_stimulus = Stimulus(
            substance = 'Sorbitol',
            amount = formData['sorbitol_amount'],
            unit = 'mM',
            targets = ['Sorbitol_out'],
            timings = [ int( e ) for e in formData['sorbitol_timing'].split(',') ],
            active = formData['sorbitol_active']
        )
        # if formData['sorbitol_active'] and isStimulusAffectingSimulation(sorbitol_stimulus, ex):
        ex.stimuli.append(sorbitol_stimulus)

        return ex

def isStimulusAffectingSimulation(stimulus, simulation):
    assert isinstance(stimulus, Stimulus)
    assert isinstance(simulation, Ex)

    return set(stimulus.targets).issubset(simulation.getOdeNames())

