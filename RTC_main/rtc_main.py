import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import time

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP], suppress_callback_exceptions= True)

# Layout of the app
app.layout = dbc.Container([

	dbc.Row([
		dbc.Col(html.Div([ # Sidebar
			html.H2('Sidebar'),
			html.Hr(),
			dcc.Dropdown( # Dropdown menu
				id= 'connector-dropdown',
				options= [
				{'label': 'IP', 'value': 'IP_connector'},
				{'label' : 'TCP', 'value' : 'TCP_connector'}
				],
				value= 'IP_connector'), # Default option on launch

			html.Div(id= 'input-fields', children= []), # Dynamic input field
			html.Button('Connect', id= 'connector-button', n_clicks= 0),
			], style={'padding' : '20px', 'backgroundColor' : '#f8f9fa', 'height': '100vh'}), width= 2),


		dbc.Col(html.Div([ # Main content area
			html.H2('Main content'),
			html.Hr(),
			html.Div(id= 'output', children=[]),
			], style= {'padding': '20px'}), width = 10
		)
	])
	], fluid= True)

# Callback to dynamically change input fields based on source
@app.callback(
	Output(component_id= 'input-fields', component_property= 'children'),
	Input(component_id= 'connector-dropdown', component_property= 'value')
	)

def update_input_fields(connector_type):

	if connector_type == 'IP_connector':
		return html.Div([
			dcc.Input(id= 'IP_input', type= 'text', placeholder= 'Enter IP address')
		])

	elif connector_type == 'TCP_connector':
		return html.Div([
				dcc.Input(id= 'TCP1_input', type= 'text', placeholder= 'Enter TCP1 address'),
				dcc.Input(id= 'TCP2_input', type= 'text', placeholder= 'Enter TCP2 address')
		])
	else:
		return html.Div()

# Callback to retrieve data and upate the main content
@app.callback(
	Output(component_id= 'output', component_property= 'children'),
	Input(component_id= 'connector-button', component_property= 'n_clicks'),
	State(component_id= 'connector-dropdown', component_property= 'value'),
	State(component_id= 'IP_input', component_property= 'value'),
	State(component_id= 'TCP1_input', component_property= 'value'),
	State(component_id= 'TCP2_input', component_property= 'value'),
	prevent_initial_call = True
)

def retrieve_data(n_clicks, connector_type, IP_input, TCP1_input, TCP2_input):
	if n_clicks > 0:
		print('success!')
		if connector_type == 'IP_connector':
			print('IP success!')

		elif connector_type == 'TCP_connector':
			print('TCP success!')

# Run app
if __name__ == '__main__':
	app.run_server(debug= True)
