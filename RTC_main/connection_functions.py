import numpy as np
from datetime import datetime
import requests
import pandas as pd
from sqlite_handler import sqlite_connect

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
    'dummy_connector': dummy_connect_dict
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