#!/bin/bash

# uncomment and replace with the real path it if you use the virtual environment
#source $path_of_virtualenv/bin/activate

pip install -r requirements.txt

python chi_annotator/webui/webuiapis/manage.py runserver