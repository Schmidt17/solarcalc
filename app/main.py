from flask import Flask, render_template, request
import json
import pandas as pd
import uuid
from random import randint

from solar_calculation.solar_benefits import calculate_solar_benefits
from solar_calculation.solar_cell import SolarCell


app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        results_dict = process(request.form)

        # return render_template('results.html', input_dict=request.form, results_dict=results_dict)
        return render_template('progress.html', task_id=str(uuid.uuid4()))


@app.route("/status/<task_id>", methods=('GET',))
def get_status(task_id):
    finished = (randint(0, 3) == 0)

    if finished:
        return json.dumps({'task_id': task_id, 'status': 'finished', 'resource': '/result'}), 303
    else:
        return json.dumps({'task_id': task_id, 'status': 'running', 'retry_after_s': 2}), 200


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

    return results_dict
