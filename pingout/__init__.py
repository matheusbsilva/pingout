import os
from uuid import uuid4

from flask import Flask
from flask import jsonify
from flask import Response

from pingout.db import connect_to_database
from pingout.db import connect_to_collection
from pingout.utils import validate_uuid


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

    @app.route("/<string:pingout_uuid>/ping", methods=['POST'])
    def ping(pingout_uuid):
        if validate_uuid(pingout_uuid):
            pingout = collection.find_one({'uuid': pingout_uuid})
            if pingout:
                if len(pingout['pings']) == 0:
                    collection.update_one({'uuid': pingout_uuid},
                                          {'$push': {'pings': {
                                              'count': 1, 'date': 0}}})
                else:
                    count = pingout['pings'][-1]['count']
                    collection.update_one({'uuid': pingout_uuid},
                                          {'$push': {'pings': {
                                              'count': count+1, 'date': 0}}})
                return Response(status=201)
            else:
                response = jsonify(errors='Pingout not found')
                response.status_code = 404
                return response
        else:
            response = jsonify(errors='Bad format uuid')
            response.status_code = 400
            return response

    return app
