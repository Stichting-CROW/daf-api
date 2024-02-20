import os
from flask import Flask, request, jsonify, g
from psycopg2.pool import SimpleConnectionPool
import daf_stats

app = Flask(__name__)

conn_str = f"dbname={os.getenv('DB_NAME')}"

if "DB_HOST" in os.environ:
    conn_str += " host={} ".format(os.environ['DB_HOST'])
if "DB_USER" in os.environ:
    conn_str += " user={}".format(os.environ['DB_USER'])
if "DB_PASSWORD" in os.environ:
    conn_str += " password={}".format(os.environ['DB_PASSWORD'])
if "DB_PORT" in os.environ:
    conn_str += " port={}".format(os.environ['DB_PORT'])

pgpool = SimpleConnectionPool(minconn=1, 
        maxconn=5, 
        dsn=conn_str)

def get_db():
    if 'db' not in g:
        g.db = pgpool.getconn()
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        pgpool.putconn(db)

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
    results = daf_stats.get_number_of_bikes_registered_in_total(get_db(), gm_code)
    return jsonify(results)

@app.route('/stats/events/overview', methods=['GET'])
def handle_event_stats():
    gm_code = request.args.get('gm_code')
    if not gm_code:
        raise InvalidUsage("No gm_code specified.", status_code=400)
    results = daf_stats.get_number_of_bikes_in_depot(get_db(), gm_code)
    return jsonify(results)

@app.route('/stats/events/checkx', methods=['GET'])
def handle_event_stats_checkx():
    gm_code = request.args.get('gm_code')
    if not gm_code:
        raise InvalidUsage("No gm_code specified.", status_code=400)
    results = daf_stats.get_stats_checkx(get_db(), gm_code)
    return jsonify(results)

if __name__ == '__main__':
    app.run()
