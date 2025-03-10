from dash import *
import dash_bootstrap_components as dbc
import plotly.express as px

import connection_functions as confunc

# Initialize Dash app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Layout of the app
app.layout = dbc.Container(
    [
        dcc.Interval(id='data_interval', interval=1000, disabled=True), # Interval object which triggers data update
        dcc.Store(id='data_store', storage_type='memory'), # Stores newest row of DataFrame, triggers updating graphs
        dcc.Store(id='data_longterm_store', storage_type='memory'), # Full DataFrame storage for if user wants to save their data
        dcc.Store(id= 'graph_configs_store', data={}), # Stores the configuration of each graph
        dcc.Store(id= 'connection_config', data=[]), # Stores data about the connection, like IP address, port
    
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [  # Sidebar with connection options
                            html.H2('Sidebar'),
                            html.Hr(),
                            dcc.Dropdown(  # Connector dropdown menu
                                id='connector-dropdown',
                                options=[
                                    {'label': 'IP', 'value': 'IP_connector'},
                                    {'label': 'TCP', 'value': 'TCP_connector'},
                                    {'label': 'SQLite', 'value': 'SQLite_connector'},
                                    {'label': 'Wikimedia Views', 'value': 'wikimedia_connector'},
                                    {'label': 'test connector', 'value': 'dummy_connector'}
                                ],
                                value='IP_connector',
                            ),  # Default option on launch
                            html.Div(
                                id='input-fields', children=[]
                            ),  # Dynamic input field(s) for each dropdown option
                            html.Button('Connect', id='connector-button', n_clicks=0),
                            dcc.Input(id='interval_input', type='number', placeholder='update interval (s)'), # Input object for selecting how often the user wants the graphs to update (default 1 second)
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
                        [  # Main content area for displaying graphs and creating graphs
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
    ],
    fluid=True,
)

# Callback for triggering the 'data_interval' dcc.Interval 'object. 
# By default 1 second or when invalid values are given. 
# Else defined by the 'interval_input' dcc.Input object.
@app.callback(
    Output(component_id='data_interval', component_property= 'interval'),
    Input(component_id='interval_input', component_property= 'value')
)
def update_interval_time(input):
    try:
        input = input * 1000
        return input
    except:
        return 1000

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
                    placeholder='http://127.0.0.1:5000',
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

    elif connector_type == 'dummy_connector':
        return html.Div(
            [
                dcc.Input(
                    id={'index': 'dummy_input', 'type': 'connection_input'},
                    type= 'text',
                    placeholder= 'Enter random text/numbers'
                )
            ]
            )
    elif connector_type == 'SQLite_connector':
        return html.Div(
            [
                dcc.Input(
                    id={'index': 'db_name', 'type': 'connection_input'},
                    type='text',
                    placeholder='Enter database name (e.g., sensor_data.db)',
                ),
                html.Br(),
                dcc.Input(
                    id={'index': 'table_name', 'type': 'connection_input'},
                    type='text',
                    placeholder='Enter table name (e.g., sensor_readings)',
                )
            ]
        )
    elif connector_type == 'wikimedia_connector':
        return html.Div([
            html.P("No configuration needed - will cycle through pageview files automatically")
        ])
    else:
        return html.Div()

# Callback for creating the interface for creating graphs
# Interface handler, generates the interface for adding X and Y-variable options for future graphs
@app.callback(
    Output(component_id='main_content', component_property='children'),
    Output(component_id='data_interval', component_property='disabled'),
    Output(component_id='connection_config', component_property='data'),
    Input(component_id='connector-button', component_property='n_clicks'),
    State(component_id='connector-dropdown', component_property='value'),
    State({'type': 'connection_input', 'index': ALL}, 'id'),
    State({'type': 'connection_input', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def setup_interface(n_clicks, connector_type, connection_id, connection_input):
    if n_clicks > 0:
        return html.Div([
            html.Div([
                # These dropdowns will be populated by the retrieve_data callback
                dcc.Dropdown(id='dropdown_X', options=[], value=None),
                dcc.Dropdown(id='dropdown_Y', options=[], value=None),
                dcc.Dropdown(
                    id='dropdown_graph_type',
                    options=[
                        {'label': 'Line plot', 'value': 'line'},
                        {'label': 'Bar chart', 'value': 'bar'},
                        {'label': 'Scatter plot', 'value': 'scatter'}
                    ],
                    value='line'
                ),
                html.Button('Add graph', id='add_graph_button', n_clicks=0),
                html.Hr(),
                html.Div(id="graph_content_area", children=[])
            ])
        ]), False, connection_input
    return dash.no_update, True, []

# Callback for retrieving data
# Also updates dropdown options so that new X and Y-variables are detected
@app.callback(
    Output(component_id='data_store', component_property='data'),
    Output(component_id='data_longterm_store', component_property='data'),
    Output(component_id='dropdown_X', component_property='options'),
    Output(component_id='dropdown_Y', component_property='options'),
    Output(component_id='dropdown_X', component_property='value'),
    Output(component_id='dropdown_Y', component_property='value'),
    Input(component_id='data_interval', component_property='n_intervals'),
    State({'type': 'connection_input', 'index': ALL}, 'id'),
    State(component_id='connection_config', component_property='data'),
    State(component_id='connector-dropdown', component_property='value'),
    State(component_id='data_longterm_store', component_property='data'),
    State(component_id='dropdown_X', component_property='value'),
    State(component_id='dropdown_Y', component_property='value'),
    prevent_initial_call=True
)
def retrieve_data(interval, connector_id, connection_config, connector_type, longterm_data, current_x, current_y):
    try:
        # Get new data point
        values = confunc.get_data_from_connector(connector_type, connection_config)
        
        # Get available columns for dropdowns
        columns = list(values.keys())
        dropdown_options = [{'label': col, 'value': col} for col in columns]
        
        # Initialize or update longterm_data
        if not longterm_data:
            longterm_data = []
        longterm_data.append(values)
        
        # Set default values for dropdowns if they're not already set
        if current_x is None or current_y is None:
            default_x = columns[0] if columns else None
            default_y = columns[1] if len(columns) > 1 else columns[0]
        else:
            default_x = current_x
            default_y = current_y
            
        return (
            values,                  # data_store
            longterm_data,          # data_longterm_store
            dropdown_options,        # dropdown_X options
            dropdown_options,        # dropdown_Y options
            default_x,              # dropdown_X value
            default_y               # dropdown_Y value
        )
        
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return [0], [0], [], [], None, None


# Callback to add a new graph div when add graph is clicked
# When either add_graph_button or dynamic_delete_button is triggered
# Either add a new graph child to the children of graph_content_area
# Or delete the child based on index and update the children of graph_content_area
@app.callback(
    Output(component_id= 'graph_content_area', component_property= 'children'),
    Output(component_id= 'graph_configs_store', component_property= 'data'),
    Input(component_id= 'add_graph_button', component_property= 'n_clicks'),
    Input({'type': 'dynamic_delete_button', 'index': ALL}, 'n_clicks'),
    State(component_id= 'dropdown_X', component_property= 'value'),
    State(component_id= 'dropdown_Y', component_property= 'value'),
    State(component_id= 'dropdown_graph_type', component_property= 'value'),
    State(component_id= 'graph_content_area', component_property= 'children'),
    State(component_id= 'data_store', component_property= 'data'),
    State(component_id= 'graph_configs_store', component_property= 'data'),
    prevent_initial_call= True
)

def add_delete_graph(n_clicks, _, x, y, graph_type, div_children, data, graph_config):
    if n_clicks > 0 and ctx.triggered_id == 'add_graph_button':

        graph_config[str(n_clicks)] = [x, y]

        x_data = [data[x]] 
        y_data = [data[y]]
        data = {x : x_data, y: y_data}

        if graph_type == 'line':
            fig = px.line(data, x= x, y= y)
            graph = dcc.Graph(id={'type': 'dynamic_graph', 'index': n_clicks}, figure= fig)
        elif graph_type == 'bar':
            fig = px.bar(data, x= x, y= y)
            graph = dcc.Graph(id={'type': 'dynamic_graph', 'index': n_clicks}, figure= fig)
        elif graph_type == 'scatter':
            fig = px.scatter(data, x= x, y= y)
            graph = dcc.Graph(id={'type': 'dynamic_graph', 'index': n_clicks}, figure= fig)

        new_child = html.Div(id= {'type': 'dynamic_graph_div', 'index': n_clicks},
        children=[
            graph,
            html.Button('Delete graph', id={'type': 'dynamic_delete_button', 'index': n_clicks}),
            html.Hr()
        ])
        div_children.append(new_child)

    elif n_clicks > 0 and ctx.triggered_id['type'] == 'dynamic_delete_button':
        del graph_config[str(ctx.triggered_id["index"])]

        delete_index = ctx.triggered_id["index"]
        div_children = [
            child for child in div_children
            if "'index': " + str(delete_index) not in str(child)
        ]

    return div_children, graph_config


# Callback to extend data to each graph that exists
@app.callback(
    Output({'type': 'dynamic_graph', 'index': MATCH}, 'figure'),
    Input(component_id= 'data_store', component_property= 'data'),
    State({'type': 'dynamic_graph', 'index': MATCH}, 'id'),
    State(component_id= 'graph_configs_store', component_property= 'data'),
    prevent_initial_call=True
)

def update_data(data_store, graph_id, graph_configs):

    # Extract the index from the graph_id
    index = graph_id['index']

    # Retrieve the configuration for the current graph
    config = graph_configs.get(str(index), None)

    if config:
        x_var, y_var = config
        x_data = data_store.get(x_var, [])
        y_data = data_store.get(y_var, [])

        patched_figure = Patch()

        patched_figure["data"][0]["x"].append(x_data)
        patched_figure["data"][0]["y"].append(y_data)
        
        return patched_figure

    else:
        return dash.no_update

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
