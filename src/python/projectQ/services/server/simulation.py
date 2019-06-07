import os
from sqlalchemy import func, desc

from projectQ.packages.db import Ex, Model, InitialValueSet, ParameterSet, Impulse, Stimulus
from projectQ.packages.values import SimulationTypes


def getScheduledSimulations(session):
    return session.query(Ex) \
            .filter(Ex.finished_at == None) \
            .order_by(desc(Ex.started_at)) \
            .all()

def getFinishedSimulations(session):
    return session.query(Ex) \
            .filter(Ex.finished_at != None) \
            .order_by(desc(Ex.started_at)) \
            .all()

def getSimulationFromFormData(session, formData):
    modelType = SimulationTypes(formData['model'])

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

    if ex.isAnyOf([SimulationTypes.combined, SimulationTypes.ion]):
        ex.impulses.append(Impulse(
            substance = 'Glucose',
            start = formData['glucose_impulse_start'],
            stop = formData['glucose_impulse_stop']
        ))

    if ex.isOfType(SimulationTypes.hog):
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
    if formData['kcl_active'] and isStimulusAffectingSimulation(kcl_stimulus, ex):
        ex.stimuli.append(kcl_stimulus)

    nacl_stimulus = Stimulus(
        substance = 'NaCl',
        amount = formData['nacl_amount'],
        unit = 'mM',
        targets = ['Na_out', 'Cl_out'],
        timings = [ int( e ) for e in formData['nacl_timing'].split(',') ],
        active = formData['nacl_active']
    )
    if formData['nacl_active'] and isStimulusAffectingSimulation(nacl_stimulus, ex):
        ex.stimuli.append(nacl_stimulus)

    sorbitol_stimulus = Stimulus(
        substance = 'Sorbitol',
        amount = formData['sorbitol_amount'],
        unit = 'mM',
        targets = ['Sorbitol_out'],
        timings = [ int( e ) for e in formData['sorbitol_timing'].split(',') ],
        active = formData['sorbitol_active']
    )
    if formData['sorbitol_active'] and isStimulusAffectingSimulation(sorbitol_stimulus, ex):
        ex.stimuli.append(sorbitol_stimulus)

    return ex

def isStimulusAffectingSimulation(stimulus, simulation):
    assert isinstance(stimulus, Stimulus)
    assert isinstance(simulation, Ex)

    return set(stimulus.targets).issubset(simulation.getOdeNames())

