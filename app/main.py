from flask import Flask, render_template, request
import json
import pandas as pd

from solar_calculation.solar_benefits import calculate_solar_benefits
from solar_calculation.solar_cell import SolarCell


app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        results_dict = process(request.form)

        return render_template('results.html', input_dict=request.form, results_dict=results_dict)


def process(input_dict):
    longitude, latitude = json.loads(input_dict['coordinates'])

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
