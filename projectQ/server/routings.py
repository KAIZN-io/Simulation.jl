import json
from flask import Blueprint, render_template, redirect

from messageQueue import mq, eventCreators
from db import sessionScope
from server.simulation import getSimulationFromFormData, getScheduledSimulations, getFinishedSimulations
from server.form import SimulationForm


routes = Blueprint('routes', __name__)

@routes.route('/app/',  methods=['GET'])
@routes.route('/app/<path:path>',  methods=['GET'])
def app( path='' ):
    return render_template('app.html')

@routes.route('/',  methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@routes.route('/simulation/neu',  methods=['GET', 'POST'])
def start():
    form = SimulationForm()

    if form.validate_on_submit():

        with sessionScope() as session:
            simulation = getSimulationFromFormData(session, form.data)
            session.commit()

            # emit event that the simulations ist started
            mq.emit(eventCreators.simulationScheduled(simulation))

        return redirect('/simulation')

    else:
        return render_template(
            'simulation/form.html',
            form=form,
            was_validated=True
        )

@routes.route('/simulation')
def running():

    with sessionScope() as session:
        scheduled_simulations = getScheduledSimulations(session)
        finished_simulations = getFinishedSimulations(session)

        return render_template(
            'simulation/overview_active.html',
            scheduled_simulations=scheduled_simulations,
            finished_simulations=finished_simulations
        )

