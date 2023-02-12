from flask import Flask, render_template, request
import json
import pandas as pd
import uuid
from random import randint

from rq import Queue
from rq.job import Job
from worker import conn

from solar_calculation.solar_benefits import calculate_solar_benefits
from solar_calculation.solar_cell import SolarCell


app = Flask(__name__)

job_queue = Queue(connection=conn)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        job = job_queue.enqueue_call(
            func=process,
            args=(request.form,),
            result_ttl=5000
        )
        task_id = job.get_id()
        # return render_template('results.html', input_dict=request.form, results_dict=results_dict)
        return render_template('progress.html', task_id=task_id)


@app.route("/status/<task_id>", methods=('GET',))
def get_status(task_id):
    job = Job.fetch(task_id, connection=conn)

    if job.is_finished:
        return json.dumps({'task_id': task_id, 'status': 'finished', 'resource': app.url_for('get_result', task_id=task_id, _external=True)}), 303
    else:
        return json.dumps({'task_id': task_id, 'status': 'running', 'retry_after_s': 2}), 200

@app.route("/result/<task_id>", methods=('GET',))
def get_result(task_id):
    job = Job.fetch(task_id, connection=conn)

    if job.is_finished:
        return render_template('results.html', input_dict=job.result['inputs'], results_dict=job.result['results'])
    else:
        return json.dumps({'error': 'Result not available'}), 404


def process(input_dict: dict) -> dict:
    """Interprets the dict with the user inputs and feeds it to the results calculation

    Note that this implements a simple input processing for first testing. It is
    not yet stable against malformed inputs and might crash.
    
    Args:
        input_dict: The dictionary with form data as received from the client

    Returns:
        A dict with the results of the solar benefit calculation
    """
    latitude = float(input_dict['location-latitude'])
    longitude = float(input_dict['location-longitude'])

    start_day = pd.Timestamp(input_dict['date-start'])
    end_day = pd.Timestamp(input_dict['date-end'])

    solar_cells = [
        SolarCell(
            float(input_dict['input-cell-1-inclination']),
            float(input_dict['input-cell-1-azimuth']),
            1e-3 * float(input_dict['input-cell-1-power'])
        )
    ]

    results_dict = calculate_solar_benefits(
        latitude=latitude,
        longitude=longitude,
        start_day=start_day,
        end_day=end_day,
        solar_cells=solar_cells
    )

    return {'inputs': input_dict, 'results': results_dict}
