"""
DPMB Tram Trips - Python Flask Backend
Alternative to Node.js server for running the application
"""

from flask import Flask, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import re
import os

app = Flask(__name__)
CORS(app)

# Configuration
LOGS_DIR = os.getenv('LOGS_DIR', r'G:\Suli\DPMB-bot\logs\2026-04-14')
PORT = int(os.getenv('PORT', 3001))
DEBUG = os.getenv('DEBUG', False)

# Global cache
data_cache = {
    'lines': {},
    'all_trips': [],
    'last_updated': None
}


def parse_trip_file(file_path):
    """Parse a trip log file and extract start/end times, destination"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.strip().split('\n')
        trips = []
        current_trip = None
        
        for line in lines:
            # Pattern: YYYY-MM-DD HH:MM:SS | START/END | details
            match = re.match(r'^([\d\-\s:]+)\s*\|\s*(START|END)\s*\|(.*)$', line)
            if not match:
                continue
            
            timestamp = match.group(1).strip()
            event_type = match.group(2)
            details = match.group(3)
            
            # Parse details
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


def process_all_trips():
    """Process all trip files from directory"""
    lines = {}
    all_trips = []
    
    try:
        if not Path(LOGS_DIR).exists():
            print(f"Error: Directory not found: {LOGS_DIR}")
            return data_cache
        
        for file_path in Path(LOGS_DIR).glob('*.txt'):
            if file_path.name == 'placeholder.txt':
                continue
            
            # Parse filename: XXXXX.txt
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
        
        # Sort trips within each line by start time
        for line_num in lines:
            lines[line_num].sort(
                key=lambda t: datetime.strptime(t['start_time'], '%Y-%m-%d %H:%M:%S')
            )
        
        data_cache['lines'] = lines
        data_cache['all_trips'] = all_trips
        data_cache['last_updated'] = datetime.now()
        
        print(f"Processed {len(lines)} lines with {len(all_trips)} total trips")
        return data_cache
    
    except Exception as e:
        print(f"Error processing trips: {e}")
        return data_cache


def get_lines():
    """Get all available lines"""
    lines = data_cache['lines']
    return [
        {
            'lineNum': int(num),
            'tripCount': len(trips)
        }
        for num, trips in lines.items()
    ]


def get_trips_for_line(line_num):
    """Get trips for specific line"""
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


# API Routes

@app.route('/api/lines', methods=['GET'])
def api_lines():
    """Get all available lines"""
    try:
        lines = get_lines()
        return jsonify({
            'success': True,
            'data': lines,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/lines/<int:line_num>/trips', methods=['GET'])
def api_trips(line_num):
    """Get trips for specific line"""
    try:
        trips = get_trips_for_line(line_num)
        return jsonify({
            'success': True,
            'line': line_num,
            'trips': trips,
            'count': len(trips),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get statistics"""
    try:
        cache = data_cache
        return jsonify({
            'success': True,
            'stats': {
                'totalLines': len(cache['lines']),
                'totalTrips': len(cache['all_trips']),
                'lastUpdated': cache['last_updated'].isoformat() if cache['last_updated'] else None
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Serve frontend or API"""
    if path.startswith('api/'):
        return jsonify({'success': False, 'error': 'Not found'}), 404
    
    # Serve frontend files
    if path and Path(f'../frontend/{path}').exists():
        return send_from_directory('../frontend', path)
    
    # Serve index.html
    try:
        with open('../frontend/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "Frontend not found", 404


if __name__ == '__main__':
    print(f"Loading trips from: {LOGS_DIR}")
    process_all_trips()
    
    print(f"DPMB Trips backend server running on http://localhost:{PORT}")
    print(f"API available at http://localhost:{PORT}/api")
    
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
