#!/bin/bash
source /home/protected/$1.config
source /home/protected/virtualenv/bin/activate
export APP_ENVIRONMENT=$1
cd /home/protected/site
gunicorn -p 8000 tftwsgi:app
