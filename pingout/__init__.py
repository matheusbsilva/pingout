import os
from flask import Flask
from flask import request
from flask import Response


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        if request.method == 'POST':
            return Response(status=201)
        else:
            return "PINGOUT"

    return app

