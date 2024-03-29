from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        return render_template('results.html', input_dict=request.form, results_dict={})
