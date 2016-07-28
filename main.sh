#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)
echo $PYTHONPATH

python3 ui/manage.py makemigrations
python3 ui/manage.py makemigrations ui_sim_interface
python3 ui/manage.py migrate
python3 ui/manage.py runserver
