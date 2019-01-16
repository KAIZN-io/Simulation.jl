from flask import Flask, render_template, redirect

from simulation_manager import SimulationManager
from simulation_form import SimulationForm


app = Flask('ProjectQ', template_folder='web-interface/templates')
sm = SimulationManager()


@app.route('/',  methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/simulation/neu',  methods=['GET', 'POST'])
def start():
    form = SimulationForm()
    if form.validate_on_submit() and not sm.has_running_simulation():
        sm.start_new_simulation(data=form.data)
        return redirect('/simulation')
    return render_template(
        'simulation/form.html',
        form=form,
        was_validated=True,
        has_running_simulation=sm.has_running_simulation()
    )


@app.route('/simulation')
def running():
    running_simulations = sm.get_running_simulations()
    return render_template('simulation/overview_active.html', running_simulations=running_simulations)
