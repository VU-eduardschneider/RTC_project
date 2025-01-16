import numpy as np
from datetime import datetime
import requests
import pandas as pd
from sqlite_handler import sqlite_connect
from collections import defaultdict

class FileSimulator:
    def __init__(self):
        self.current_file_index = 0
        self.file_pattern = "Cases/Case 2 - PageViews data/data/projectviews-20250101-{:06d}"
        self.times = ["000000", "010000", "020000", "030000", "040000", 
                     "050000", "060000", "070000", "080000", "090000"]
        
    def get_next_file(self):
        if self.current_file_index >= len(self.times):
            self.current_file_index = 0  # Reset to start
            
        filename = self.file_pattern.format(int(self.times[self.current_file_index]))
        self.current_file_index += 1
        return filename

def extract_country_code(project):
    """Extract country code from project name"""
    # Handle special cases first
    print(project)
    if project.startswith('www.'):
        return 'WW'  # Worldwide
    if project.startswith('commons.'):
        return 'WW'
    if project.startswith('wikidata.'):
        return 'WW'
        
    # Regular country codes
    parts = project.split('.')
    if not parts:
        return 'OTHER'
    return parts[0].upper()

def process_pageview_data(file_content):
    """Process the pageview data into a structured format"""
    country_stats = defaultdict(lambda: {'total': 0, 'mobile': 0, 'desktop': 0})
    print
    
    for line in file_content.split('\n'):
        if not line.strip():
            continue
            
        parts = line.split(' - ')
        
        project = parts[0]

        views = int(parts[1][0:-1])

        print('project:', project, 'views:', views)
        views = int(views)
        
        country_code = extract_country_code(project)
        country_stats[country_code]['total'] += views
        
        if '.m.' in project:
            country_stats[country_code]['mobile'] += views
        else:
            country_stats[country_code]['desktop'] += views

    # Convert to simple dict and calculate totals
    current_time = datetime.now().strftime('%H:%M:%S')
    total_views = sum(stats['total'] for stats in country_stats.values())
    print('total_views:', total_views)
    
    # Find top 10 countries by total views
    top_countries = sorted(
        country_stats.items(), 
        key=lambda x: x[1]['total'], 
        reverse=True
    )[:10]
    
    result = {
        'Time': current_time,
        'Total_Views': total_views,
        'Mobile_Views': sum(stats['mobile'] for stats in country_stats.values()),
        'Desktop_Views': sum(stats['desktop'] for stats in country_stats.values()),
    }
    
    # Add top 10 countries data
    for country_code, stats in top_countries:
        result[f'{country_code}_Views'] = stats['total']
        result[f'{country_code}_Mobile'] = stats['mobile']
        result[f'{country_code}_Desktop'] = stats['desktop']
        result[f'{country_code}_Mobile_Pct'] = round((stats['mobile'] / stats['total'] * 100 if stats['total'] > 0 else 0), 2)
    
    return result

file_simulator = FileSimulator()

def wikimedia_connect(dummy_arg=None):
    """
    Simulates a connection by reading the next file in sequence
    Returns processed pageview statistics including country-specific data
    """
    try:
        filename = file_simulator.get_next_file()
        data = process_pageview_data(open(filename).read())
        return data
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def IP_connect(ip_address):
    """
    Connects to IP address and retrieves current data
    Expected format: 'http://127.0.0.1:5000'
    """
    try:
        response = requests.get(f"{ip_address}/data")
        if response.status_code == 200:
            data = response.json()
            # Add current time to the data
            data['Time'] = datetime.now().strftime('%H:%M:%S')
            return data
        else:
            raise ConnectionError(f"Failed to retrieve data: Status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Connection error: {e}")
        return None

def TCP_connect(tcp_address):
	return 0

def dummy_connect_pd(dummy_address):
	columns = ['A', 'B', 'C', 'D', 'E']

	random_values = [np.random.rand() for i in range(5)]

	df = pd.DataFrame([random_values], columns= columns)

	return df

def dummy_connect_dict(dummy_address):
	columns = ['Time', 'A', 'B', 'C', 'D', 'E']

	random_values = [np.random.rand() for i in range(5)]

	dict_vals = {}

	current_time = datetime.now().strftime('%H:%M:%S')
	dict_vals[columns[0]] = current_time

	for i in range(1, len(columns)):
		dict_vals[columns[i]] = random_values[i-1]

	return dict_vals

# Dictionary mapping connector types to their functions
CONNECTOR_TYPES = {
    'IP_connector': IP_connect,
    'TCP_connector': TCP_connect,
    'SQLite_connector': sqlite_connect,
    'dummy_connector': dummy_connect_dict,
    'wikimedia_connector': wikimedia_connect
}

def get_data_from_connector(connector_type, connection_config):
    """
    Get data using the specified connector type
    Args:
        connector_type (str): Type of connector to use
        connection_config: Configuration for the connector
    Returns:
        dict: Data from the connector
    """
    if connector_type in CONNECTOR_TYPES:
        return CONNECTOR_TYPES[connector_type](connection_config)
    else:
        raise ValueError(f"Unknown connector type: {connector_type}")