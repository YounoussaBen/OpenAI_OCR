#!/bin/bash

# Activate the virtual environment
source env/bin/activate

# Start the Flask application with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.api:app


docker run -p 5000:5000 my-flask-app