import os
from uuid import uuid4
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=['GET'])
    def root():
        return "PINGOUT"

    @app.route("/create-pingout", methods=['POST'])
    def create_pingout():
        uuid = uuid4()
        response = jsonify({'uuid': uuid.hex})
        response.status_code = 201
        return response

    return app
