from flask import Blueprint, render_template, redirect

import simulation_manager as sm
import message_queue as mq
from simulation_form import SimulationForm
from db import sessionScope


routes = Blueprint('routes', __name__)

@routes.route('/',  methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@routes.route('/simulation/neu',  methods=['GET', 'POST'])
def start():
    form = SimulationForm()

    if form.validate_on_submit():

        with sessionScope() as session:
            simulation = sm.getSimulationFromFormData(session, form.data)
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
        scheduled_simulations = sm.getScheduledSimulations(session)
        finished_simulations = sm.getFinishedSimulations(session)

        return render_template(
            'simulation/overview_active.html',
            scheduled_simulations=scheduled_simulations,
            finished_simulations=finished_simulations
        )

