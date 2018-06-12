import os
from uuid import uuid4

from flask import Flask
from flask import jsonify

from pingout.db import connect_to_database
from pingout.db import connect_to_collection


def create_app(test_config=None, db=connect_to_database()):
    app = Flask(__name__, instance_relative_config=True)
    collection = connect_to_collection(db)

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
        collection.insert_one({'uuid': uuid.hex, 'pings': []})
        response = jsonify({'uuid': uuid.hex})
        response.status_code = 201
        return response

    return app
