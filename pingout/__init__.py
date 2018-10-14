import os
import datetime
from uuid import uuid4

from flask import Flask
from flask import jsonify
from flask import Response
from flask import request
from flask import redirect
from flask import render_template
from flask import send_from_directory
from dateutil import parser

from pingout.db import connect_to_database
from pingout.db import connect_to_collection
from pingout.utils import validate_uuid
from pingout.utils import from_json_to_csv
from pingout.filters import filter_occurrences_ping_range_date


SECRET_KEY = os.environ.get('APP_SECRET_KEY', 'dev')


def create_app(test_config=None, db=connect_to_database()):
    app = Flask(__name__, template_folder='../pingout/templates')
    app.config.from_mapping(SECRET_KEY=SECRET_KEY)

    collection = connect_to_collection(db)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def root():
        return "PINGOUT!!! Up and running"

    @app.route("/<string:pingout_uuid>", methods=['GET'])
    def get_pingouts_occur_range_date(pingout_uuid):
        if validate_uuid(pingout_uuid):
            pingout = collection.find_one({'uuid': pingout_uuid})
            if pingout:
                initial = request.args.get('initial_date')
                final = request.args.get('final_date')
                try:
                    initial = parser.parse(initial)
                    final = parser.parse(final)
                except TypeError:
                    return Response(status=400)
                query = filter_occurrences_ping_range_date(pingout_uuid,
                                                           collection, initial,
                                                           final)
                from_json_to_csv(query, "{}.csv".format(pingout_uuid))
                return redirect('/{}/download'.format(pingout_uuid))
            else:
                return Response(status=404)

    @app.route("/<string:pingout_uuid>/download")
    def download_filtered_file(pingout_uuid):
        if request.method == 'GET':
            filename = "{}.csv".format(pingout_uuid)
            return render_template('download.html',
                                   uuid=pingout_uuid,
                                   filename=filename)

    @app.route("/<string:pingout_uuid>/download/<path:filename>")
    def download_file(pingout_uuid, filename):
        return send_from_directory(directory='../files', filename=filename)

    @app.route("/create-pingout", methods=['POST', 'GET'])
    def create_pingout():
        if request.method == 'POST':
            uuid = uuid4()
            collection.insert_one({'uuid': uuid.hex, 'pings': []})
            response = jsonify({'uuid': uuid.hex})
            response.status_code = 201
            return response
        else:
            return Response(status=405)

    @app.route("/<string:pingout_uuid>/ping", methods=['POST'])
    def ping(pingout_uuid):
        if validate_uuid(pingout_uuid):
            pingout = collection.find_one({'uuid': pingout_uuid})
            if pingout:
                date = datetime.datetime.today().replace(second=0,
                                                         microsecond=0)
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
