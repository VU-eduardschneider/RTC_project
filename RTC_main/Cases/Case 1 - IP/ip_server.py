from flask import Flask, jsonify
import pandas as pd
import time
from threading import Thread

app = Flask(__name__)

# Global variable to store current row
current_data = {}

def load_and_stream_csv(csv_path, delay=1.0):
    """
    Loads CSV file and streams it row by row with specified delay
    """
    df = pd.read_csv(csv_path)
    row_index = 0
    
    while True:
        # Get current row as dictionary
        global current_data
        current_data = df.iloc[row_index].to_dict()
        
        # Increment row index, reset if at end
        row_index = (row_index + 1) % len(df)
        
        time.sleep(delay)

@app.route('/data', methods=['GET'])
def get_data():
    """Returns current row of data"""
    return jsonify(current_data)

def start_server(csv_path, port=5000):
    # Start the data streaming in a separate thread
    stream_thread = Thread(target=load_and_stream_csv, args=(csv_path,), daemon=True)
    stream_thread.start()
    
    # Run the Flask server
    app.run(host='127.0.0.1', port=port)

if __name__ == '__main__':
    # Replace with your CSV path
    CSV_PATH = 'feature9.csv'
    start_server(CSV_PATH)
