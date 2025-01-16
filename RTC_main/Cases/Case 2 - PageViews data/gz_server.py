import gzip
import json
import pandas as pd
from flask import Flask, jsonify
import time
from threading import Thread
import csv
from io import StringIO

app = Flask(__name__)

# Global variable to store current row
current_data = {}

def load_and_stream_gz(gz_path, delay=1.0):
    """
    Loads .gz file and streams it row by row with specified delay
    Works with both CSV and JSON formats inside the .gz file
    """
    global current_data
    
    # Try to determine if file is CSV or JSON by reading first line
    with gzip.open(gz_path, 'rt') as f:
        first_line = f.readline().strip()
        # Reset file pointer
        f.seek(0)
        
        try:
            # Try parsing as JSON first
            json.loads(first_line)
            is_json = True
        except json.JSONDecodeError:
            is_json = False

    if is_json:
        # Handle JSON lines format
        while True:
            with gzip.open(gz_path, 'rt') as f:
                for line in f:
                    current_data = json.loads(line)
                    time.sleep(delay)
    else:
        # Handle CSV format
        while True:
            with gzip.open(gz_path, 'rt') as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    current_data = row
                    time.sleep(delay)

@app.route('/data', methods=['GET'])
def get_data():
    """Returns current row of data"""
    return jsonify(current_data)

def start_server(gz_path, port=5000):
    # Start the data streaming in a separate thread
    stream_thread = Thread(target=load_and_stream_gz, args=(gz_path,), daemon=True)
    stream_thread.start()
    
    # Run the Flask server
    app.run(host='127.0.0.1', port=port)

if __name__ == '__main__':
    # Replace with your .gz file path
    GZ_PATH = 'pageviews-20240124-110000.gz'
    start_server(GZ_PATH)