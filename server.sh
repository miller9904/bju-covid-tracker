#!/bin/sh

. venv/bin/activate
export FLASK_APP=server.py
flask run