import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import time

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2("Sidebar"),
            html.Hr(),
            dcc.Dropdown(
                id='data-source-dropdown',
                options=[
                    {'label': 'Data Source 1', 'value': 'source1'},
                    {'label': 'Data Source 2', 'value': 'source2'},
                ],
                value='source1'
            ),
            html.Div(id='input-fields'),
            html.Button('Connect', id='connect-button', n_clicks=0),
        ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'height': '100vh'}), width=2),

        dbc.Col(html.Div([
            html.H2("Main Content"),
            html.Hr(),
            html.Div(id='output-data'),
        ], style={'padding': '20px'}), width=10)
    ])
], fluid=True)

# Callback to update input fields based on the selected data source
@app.callback(
    Output('input-fields', 'children'),
    Input('data-source-dropdown', 'value')
)
def update_input_fields(selected_source):
    if selected_source == 'source1':
        return html.Div([
            dcc.Input(id='source1-input', type='text', placeholder='Enter input for Source 1')
        ])
    elif selected_source == 'source2':
        return html.Div([
            dcc.Input(id='source2-input', type='text', placeholder='Enter input for Source 2')
        ])
    return html.Div()

# Callback to retrieve data and update the main content
@app.callback(
    Output('output-data', 'children'),
    Output('source1-input', 'value'),
    Output('source2-input', 'value'),
    Input('connect-button', 'n_clicks'),
    State('data-source-dropdown', 'value')
  
)
def retrieve_data(n_clicks, selected_source, source1_input, source2_input):
    if n_clicks > 0:
        if selected_source == 'source1':
            # Simulate data retrieval from Source 1
            data = retrieve_data_from_source1(source1_input)
        elif selected_source == 'source2':
            # Simulate data retrieval from Source 2
            data = retrieve_data_from_source2(source2_input)

        # Display the data as a table
        return html.Div([
            html.H3('Retrieved Data'),
            dash_table.DataTable(
                data=data.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in data.columns]
            )
        ])
    return html.Div()

# Simulated functions to retrieve data from external sources
def retrieve_data_from_source1(input_value):
    # Simulate data retrieval
    time.sleep(1)
    data = pd.DataFrame({
        'Column1': [1, 2, 3],
        'Column2': [4, 5, 6]
    })
    return data

def retrieve_data_from_source2(input_value):
    # Simulate data retrieval
    time.sleep(1)
    data = pd.DataFrame({
        'ColumnA': [7, 8, 9],
        'ColumnB': [10, 11, 12]
    })
    return data

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
