#!/bin/bash

# uncomment it if you use the virtual environment
#source /home/jialei/py_env/py3_dev/bin/activate

pip install -r ../requirements.txt

firefox ../chi_annotator/webui/static/web_util.html & python3.6 ../chi_annotator/webui/webuiapis/manage.py runserver