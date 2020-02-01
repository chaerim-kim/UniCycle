#!/bin/bash
module add python/3.4.3
source flask/bin/activate
export FLASK_APP=run.py
export FLASK_ENV=development

flask run
