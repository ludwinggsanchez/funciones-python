#!/bin/bash
# Setup and run the Flask API

cd "$(dirname "$0")"

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate venv and install requirements
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run the Flask app
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
