# api_server.py
# Flask REST API for networked database access (local network testing)
# Run this server, then point your clients to it in network mode.

from flask import Flask, request, jsonify
import db
from backend import Individual

app = Flask(__name__)

@app.route('/individuals/<table_type>', methods=['GET'])
def get_individuals(table_type):
    # Return all individuals for a table_type
    individuals = db.load_individuals(table_type)
    return jsonify([
        {
            'name': ind.name,
            'vorname': ind.vorname,
            'reisegruppe': ind.reisegruppe,
            'alter': ind.alter,
            'geschlecht': ind.geschlecht,
            'anwesend': ind.anwesend,
            'evakuiert': ind.evakuiert,
            'notiz': ind.notiz
        } for ind in individuals
    ])

@app.route('/individuals/<table_type>', methods=['POST'])
def save_individuals(table_type):
    # Overwrite all individuals for a table_type
    data = request.json
    individuals = []
    for d in data:
        ind = Individual(d['name'], d['vorname'], d['reisegruppe'], d['alter'], d['geschlecht'])
        ind.anwesend = d['anwesend']
        ind.evakuiert = d['evakuiert']
        ind.notiz = d['notiz']
        individuals.append(ind)
    db.save_individuals(table_type, individuals)
    return '', 204

@app.route('/log', methods=['GET'])
def get_log():
    # Return all log entries
    log = db.load_log()
    return jsonify([
        {'timestamp': ts, 'fullname': fullname, 'reisegruppe': reisegruppe, 'status': status}
        for ts, fullname, reisegruppe, status in log
    ])

@app.route('/log', methods=['POST'])
def add_log():
    # Add a log entry
    data = request.json
    db.add_log_entry(data['fullname'], data['reisegruppe'], data['status'])
    return '', 204

@app.route('/clear', methods=['POST'])
def clear_all():
    db.clear_all()
    return '', 204

if __name__ == '__main__':
    db.init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
