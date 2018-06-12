import os
import datetime
from uuid import uuid4

from flask import Flask
from flask import jsonify
from flask import Response
from flask import request

from pingout.db import connect_to_database
from pingout.db import connect_to_collection
from pingout.utils import validate_uuid
from pingout.filters import filter_occurrences_ping_range_date


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

    @app.route("/<string:pingout_uuid>", methods=['GET'])
    def get_pingouts_occur_range_date(pingout_uuid):
        if validate_uuid(pingout_uuid):
            pingout = collection.find_one({'uuid': pingout_uuid})
            if pingout:
                return Response(status=200)
            else:
                return Response(status=404)

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
                date = datetime.date.today()
                if len(pingout['pings']) == 0:
                    collection.update_one({'uuid': pingout_uuid},
                                          {'$push': {'pings': {
                                              'count': 1, 'date': date}}})
                else:
                    count = pingout['pings'][-1]['count']
                    collection.update_one({'uuid': pingout_uuid},
                                          {'$push': {'pings': {
                                              'count': count+1, 'date': date
                                              }}})
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
