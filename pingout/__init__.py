import os
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
        response = jsonify({'uuid': '9cc41faf294f457583afcaf79a3f98ab'})
        response.status_code = 201
        return response

    return app
