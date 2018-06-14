#!/bin/bash

# Set development to APP_ENVIRONMENT if it is unset 
export FLASK_ENV=${APP_ENVIRONMENT:=development}
export FLASK_APP=pingout
flask run --host=0.0.0.0
