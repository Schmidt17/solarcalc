from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        return render_results({}, request.form)


def render_results(results_dict, input_dict):
    input_str = json.dumps(input_dict)
    results_str = json.dumps(results_dict)

    return_html = f"Inputs:<br>{input_str}"
    return_html += f"<br><br>Results:<br>{results_str}"

    return return_html
