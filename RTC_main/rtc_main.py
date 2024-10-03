import dash
from dash import *
import dash_bootstrap_components as dbc
import pandas as pd
import time
import json

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Layout of the app
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [  # Sidebar
                            html.H2('Sidebar'),
                            html.Hr(),
                            dcc.Dropdown(  # Connector dropdown menu
                                id='connector-dropdown',
                                options=[
                                    {'label': 'IP', 'value': 'IP_connector'},
                                    {'label': 'TCP', 'value': 'TCP_connector'},
                                ],
                                value='IP_connector',
                            ),  # Default option on launch
                            html.Div(
                                id='input-fields', children=[]
                            ),  # Dynamic input field(s) for each dropdown option
                            html.Button('Connect', id='connector-button', n_clicks=0),
                        ],
                        style={
                            'padding': '20px',
                            'backgroundColor': '#f8f9fa',
                            'height': '100vh',
                        },
                    ),
                    width=2,
                ),
                dbc.Col(
                    html.Div(
                        [  # Main content area
                            html.H2('Main content'),
                            html.Hr(),
                            html.Div(id='main_content', children=[]),
                        ],
                        style={'padding': '20px'},
                    ),
                    width=10,
                ),
            ]
        ),
    	dcc.Interval(id='data_interval', interval=1000, disabled=True), # Interval object which triggers data update
    	dcc.Store(id='data_store', storage_type='memory'), # Stores newest row of DataFrame, triggers updating graphs
    	dcc.Store(id='data_longterm_store', storage_type='memory') # Full DataFrame storage for if user wants to save their data
    ],
    fluid=True,
)


# Callback to dynamically change input fields based on source
# When a connector_type is selected, replace the fields with the appropriate fields
@app.callback(
    Output(component_id='input-fields', component_property='children'),
    Input(component_id='connector-dropdown', component_property='value'),
)
def update_input_fields(connector_type):
    if connector_type == 'IP_connector':
        return html.Div(
            [
                dcc.Input(
                    id={'index': 'IP_input', 'type': 'connection_input'},
                    type='text',
                    placeholder='Enter IP address',
                )
            ]
        )

    elif connector_type == 'TCP_connector':
        return html.Div(
            [
                dcc.Input(
                    id={'index': 'TCP1_input', 'type': 'connection_input'},
                    type='text',
                    placeholder='Enter TCP1 address',
                ),
                dcc.Input(
                    id={'index': 'TCP2_input', 'type': 'connection_input'},
                    type='text',
                    placeholder='Enter TCP2 address',
                ),
            ]
        )
    # Add mor elifs for new connection types here
    else:
        return html.Div()


# Callback to retrieve data and upate the main content
# When the connector_button is clicked, add the new div for adding graphs
# And enable the dcc.Interval by disabling the 'disabled' property of data_interval
@app.callback(
    Output(component_id='main_content', component_property='children'),
    Output(component_id='data_interval', component_property='disabled'),  # MOVE THIS TO CONFIRM SCREEN WHEN CONFIRM IS DONE
    Input(component_id='connector-button', component_property='n_clicks'),
    State(component_id='connector-dropdown', component_property='value'),
    State({'type': 'connection_input', 'index': ALL}, 'id'),
    State({'type': 'connection_input', 'index': ALL}, 'value'),
    prevent_initial_call=True
)

def retrieve_data_temp(n_clicks, connector_type, custom_id, connection_input):
	connection = ''
	if n_clicks > 0:
		if connector_type:
			print(f'{connector_type.split("_")[0]} success!')
		connection_data = {custom_id[x]['index']: str(connection_input[x]) for x in range(len(connection_input))}
		connection = f'{connector_type.split("_")[0]} - {connection_data}'
	return html.Div([
	html.Div(id="graph_content_area", children= []),
	html.Div([ # Return a new 'add graph' object
		dcc.Dropdown( # Dropdown menu for the X variable
            id='dropdown_X',
            options=[
                {'label': 'variable 1', 'value': '1'},
                {'label': 'variable 2', 'value': '2'}
            ], value = '1'
        ),
        dcc.Dropdown( # Dropdown menu for the Y variable
        	id='dropdown_Y',
            options=[
                {'label': 'variable 1', 'value': '1'},
                {'label': 'variable 2', 'value': '2'}
        	], 
        	value= '1'
        ),
        dcc.Dropdown( # Dropdown menu for the plot variable
            id='dropdown_graph_type',
            options=[
                {'label': 'Line plot', 'value': '1'},
                {'label': 'Bar chart', 'value': '2'},
                {'label': 'Scatter plot', 'value': '3'}
            ], value = '1'
        ),
        html.Button('Add graph', id= 'add_graph_button', n_clicks= 0), # Add graph button
    	connection,
    	html.Hr()
    ])]), False

# Callback to retrieve and store data each time the interval passes
# When the interval is triggered, store new data into the short 'data_store'
# And store entire dataset in 'dataLlongterm_store'
@app.callback(
	Output(component_id='data_store', component_property='data'),
	Output(component_id='data_longterm_store', component_property='data'),
	Input(component_id='data_interval', component_property='n_intervals'),
	State({'type': 'connection_input', 'index': ALL}, 'id'),
	State({'type:': 'connection_input', 'index': ALL}, 'value'),
	prevent_initial_call=True
)

def retrieve_data(interval, connector_id, value):
	if connector_id[0]['index'] == None:
		print('Something is going wrong!')
		return [0], [0]

	elif connector_id[0]['index'] == 'IP_input':
		print('IP')
		return [1], [1]

	elif connector_id[0]['index'] == 'TCP1_input':
		print('TCP')
		return [2], [2]

# Callback to add a new graph div when add graph is clicked
# When either add_graph_button or dynamic_delete_button is triggered
# Either add a new graph child to the children of graph_content_area
# Or delete the child based on index and update the children of graph_content_area
@app.callback(
	Output(component_id= 'graph_content_area', component_property= 'children'),
	Input(component_id= 'add_graph_button', component_property= 'n_clicks'),
	Input({'type': 'dynamic_delete_button', 'index': ALL}, 'n_clicks'),
	State(component_id= 'dropdown_X', component_property= 'value'),
	State(component_id= 'dropdown_Y', component_property= 'value'),
	State(component_id= 'dropdown_graph_type', component_property= 'value'),
	State(component_id= 'graph_content_area', component_property= 'children'),
	prevent_initial_call= True
)

def add_delete_graph(n_clicks, _, x, y, graph_type, div_children):
	if n_clicks > 0 and ctx.triggered_id == 'add_graph_button':
		print('X:', x, 'Y:', y, 'Graph type:', graph_type, 'index:', n_clicks)
		new_child = html.Div(id= {'type': 'dynamic_graph_div', 'index': n_clicks},
		children=[
			x, y, graph_type, n_clicks,
			html.Button('Delete graph', id={'type': 'dynamic_delete_button', 'index': n_clicks}),
			html.Hr()
		])
		div_children.append(new_child)

	else:
		delete_index = ctx.triggered_id["index"]
		div_children = [
			child for child in div_children
            if "'index': " + str(delete_index) not in str(child)
		]

	return div_children

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
