# solarcalc

solarcalc is a web application that allows users to calculate the benefit of 
installing a solar power generation system at a given location. The benefit 
is calculated based on real weather data.

## Getting started

You can run the app locally for debugging (NOTE: the following instructions
are not suitable for a production release!). Start by installing [Redis](https://redis.io/), which
we use for tracking the status of the long-running server-side calculations.
Installation instructions for your platform can be found [here](https://redis.io/docs/getting-started/).


Assuming, you have a working
installation of Python 3, proceed by installing the Python dependencies:

```
$ pip install -r requirements.txt
```

Then, navigate into the `app` directory. From there, you can run a 
development server by executing

```
$ flask --app main run
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. 
Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

The server tells you that it's running on your local machine and is listening
on port 5000. Open http://127.0.0.1:5000/ in your favorite browser and you
should see the front page of solarcalc.
