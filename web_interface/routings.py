from flask import Blueprint, render_template, redirect

from simulation_manager import SimulationManager
from simulation_form import SimulationForm


sm = SimulationManager()

routes = Blueprint('routes', __name__)

@routes.route('/',  methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@routes.route('/simulation/neu',  methods=['GET', 'POST'])
def start():
    form = SimulationForm()
    if form.validate_on_submit() and not sm.has_running_simulation():
        sm.start_new_simulation(formData=form.data)
        return redirect('/simulation')
    return render_template(
        'simulation/form.html',
        form=form,
        was_validated=True,
        has_running_simulation = sm.has_running_simulation()
    )

@routes.route('/simulation')
def running():
    running_simulations = sm.get_running_simulations()
    finished_simulations = sm.get_finished_simulations()
    return render_template(
        'simulation/overview_active.html',
        running_simulations=running_simulations,
        finished_simulations=finished_simulations
    )

