from flask import Blueprint, render_template, redirect

import messageQueue as mq
from db import sessionScope
from server.simulation import getSimulationFromFormData, getScheduledSimulations, getFinishedSimulations
from server.form import SimulationForm


routes = Blueprint('routes', __name__)

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
            mq.scheduleSimulation(simulation)

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

