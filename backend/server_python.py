"""
DPMB Tram Trips - Python Flask Backend
Railway-compatible version
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import re
import os

app = Flask(__name__)
CORS(app)

# ======================
# CONFIG
# ======================

LOGS_DIR = os.getenv('LOGS_DIR', './logs')
PORT = int(os.getenv('PORT', 3001))
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# Ensure logs directory exists
logs_path = Path(LOGS_DIR)
if not logs_path.exists():
    print(f"Creating logs directory: {LOGS_DIR}")
    logs_path.mkdir(parents=True, exist_ok=True)

# ======================
# CACHE
# ======================

data_cache = {
    'lines': {},
    'all_trips': [],
    'last_updated': None
}

# ======================
# PARSER
# ======================

def parse_trip_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.strip().split('\n')
        trips = []
        current_trip = None

        for line in lines:
            match = re.match(r'^([\d\-\s:]+)\s*\|\s*(START|END)\s*\|(.*)$', line)
            if not match:
                continue

            timestamp = match.group(1).strip()
            event_type = match.group(2)
            details = match.group(3)

            destination = ''
            line_num = ''
            vehicle = ''

            for part in details.split('|'):
                if 'Cél:' in part:
                    destination = part.split('Cél:')[1].strip()
                if 'Vonal:' in part:
                    line_num = part.split('Vonal:')[1].strip()
                if 'Jármű:' in part:
                    vehicle = part.split('Jármű:')[1].strip()

            if event_type == 'START':
                current_trip = {
                    'start_time': timestamp,
                    'end_time': None,
                    'destination': destination,
                    'line': line_num,
                    'vehicle': vehicle,
                    'segments': [line_num]
                }

            elif event_type == 'END' and current_trip:
                current_trip['end_time'] = timestamp

                if current_trip['start_time'] and current_trip['end_time']:
                    trips.append(current_trip)

                current_trip = None

        return trips

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []

# ======================
# PROCESSOR
# ======================

def process_all_trips():
    lines = {}
    all_trips = []

    try:
        if not logs_path.exists():
            print(f"Logs directory missing: {LOGS_DIR}")
            return data_cache

        files = list(logs_path.glob('*.txt'))

        if not files:
            print("No log files found.")
            return data_cache

        for file_path in files:
            if file_path.name == 'placeholder.txt':
                continue

            match = re.match(r'^(\d{3})(\d{2})\.txt$', file_path.name)
            if not match:
                continue

            line_num = int(match.group(1))
            trip_num = int(match.group(2))

            trips = parse_trip_file(str(file_path))

            if trips:
                if line_num not in lines:
                    lines[line_num] = []

                for trip in trips:
                    trip['line_id'] = line_num
                    trip['trip_id'] = trip_num
                    trip['filename'] = file_path.name

                    lines[line_num].append(trip)
                    all_trips.append(trip)

        for line_num in lines:
            lines[line_num].sort(
                key=lambda t: datetime.strptime(t['start_time'], '%Y-%m-%d %H:%M:%S')
            )

        data_cache['lines'] = lines
        data_cache['all_trips'] = all_trips
        data_cache['last_updated'] = datetime.now()

        print(f"Processed {len(lines)} lines, {len(all_trips)} trips")

        return data_cache

    except Exception as e:
        print(f"Error processing trips: {e}")
        return data_cache

# ======================
# HELPERS
# ======================

def get_lines():
    return [
        {
            'lineNum': int(num),
            'tripCount': len(trips)
        }
        for num, trips in data_cache['lines'].items()
    ]


def get_trips_for_line(line_num):
    trips = data_cache['lines'].get(line_num, [])

    return [
        {
            'tripId': trip['trip_id'],
            'filename': trip['filename'],
            'startTime': trip['start_time'],
            'endTime': trip['end_time'],
            'destination': trip['destination'],
            'lines': trip['segments'],
            'vehicle': trip['vehicle']
        }
        for trip in trips
    ]

# ======================
# API
# ======================

@app.route('/api/lines')
def api_lines():
    return jsonify({
        'success': True,
        'data': get_lines(),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/lines/<int:line_num>/trips')
def api_trips(line_num):
    trips = get_trips_for_line(line_num)

    return jsonify({
        'success': True,
        'line': line_num,
        'trips': trips,
        'count': len(trips),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/stats')
def api_stats():
    return jsonify({
        'success': True,
        'stats': {
            'totalLines': len(data_cache['lines']),
            'totalTrips': len(data_cache['all_trips']),
            'lastUpdated': data_cache['last_updated'].isoformat() if data_cache['last_updated'] else None
        }
    })

# ======================
# FRONTEND
# ======================

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('api/'):
        return jsonify({'success': False, 'error': 'Not found'}), 404

    frontend_path = Path('../frontend')

    if path and (frontend_path / path).exists():
        return send_from_directory(frontend_path, path)

    try:
        return (frontend_path / 'index.html').read_text(encoding='utf-8')
    except:
        return "Frontend not found", 404

# ======================
# START
# ======================

if __name__ == '__main__':
    print(f"Loading trips from: {LOGS_DIR}")

    process_all_trips()

    print(f"Server running on port {PORT}")
    print(f"API: /api")

    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)