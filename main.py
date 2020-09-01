import os
from flask import Flask, request, jsonify
import psycopg2
import daf_stats

app = Flask(__name__)

conn_str = "dbname='daf'"
if "IP" in os.environ:
    conn_str += " host={} ".format(os.environ['IP'])
if "DB_PASSWORD" in os.environ:
    conn_str += " user=daf password={}".format(os.environ['DB_PASSWORD'])

conn = psycopg2.connect(conn_str)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/stats/bikes/overview', methods=['GET'])
def handle_bike_stats():
    gm_code = request.args.get('gm_code')
    if not gm_code:
        raise InvalidUsage("No gm_code specified.", status_code=400)
    results = daf_stats.get_number_of_bikes_registered_in_total(conn, gm_code)
    return jsonify(results)

@app.route('/stats/events/overview', methods=['GET'])
def handle_event_stats():
    gm_code = request.args.get('gm_code')
    if not gm_code:
        raise InvalidUsage("No gm_code specified.", status_code=400)
    results = daf_stats.get_number_of_bikes_in_depot(conn, gm_code)
    return jsonify(results)

@app.route('/stats/events/checkx', methods=['GET'])
def handle_event_stats_checkx():
    gm_code = request.args.get('gm_code')
    if not gm_code:
        raise InvalidUsage("No gm_code specified.", status_code=400)
    results = daf_stats.get_stats_checkx(conn, gm_code)
    return jsonify(results)

if __name__ == '__main__':
    app.run()
