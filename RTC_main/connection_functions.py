import numpy as np
from datetime import datetime

def IP_connect(ip_address):
	return 0

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
