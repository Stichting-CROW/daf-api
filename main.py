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


@app.route('/stats/bikes/overview', methods=['GET'])
def handle_bike_stats():
    results = daf_stats.get_number_of_bikes_registered_in_total(conn)
    return jsonify(results)

@app.route('/stats/events/overview', methods=['GET'])
def handle_event_stats():
    results = daf_stats.get_number_of_bikes_in_depot(conn)
    return jsonify(results)

@app.route('/stats/events/checkx', methods=['GET'])
def handle_event_stats_checkx():
    results = daf_stats.get_stats_checkx(conn)
    return jsonify(results)

if __name__ == '__main__':
    app.run()
