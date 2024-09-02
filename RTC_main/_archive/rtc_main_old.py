import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import time
import threading

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Dropdown(
        id='function-dropdown',
        options=[
            {'label': 'Function 1', 'value': 'func1'},
            {'label': 'Function 2', 'value': 'func2'},
        ],
        placeholder="Select a function"
    ),
    html.Div(id='dynamic-input-fields', **{'data-id': 'dynamic-input-fields'}),
    html.Button('Start', id='start-button', n_clicks=0, **{'data-id': 'start-button'}),
    html.Div(id='output', **{'data-id': 'output'})
], **{'data-id': 'main-div'})

def func1(param1):
    return f"Data from func1 with param1={param1}"

def func2(param2, param3):
    return f"Data from func2 with param2={param2} and param3={param3}"

@app.callback(
    Output('dynamic-input-fields', 'children'),
    Input('function-dropdown', 'value')
)
def update_input_fields(selected_function):
    if selected_function == 'func1':
        return html.Div([
            dcc.Input(id='param1', type='text', placeholder='Enter param1', **{'data-id': 'param1'}),
        ], **{'data-id': 'func1-div'})

    elif selected_function == 'func2':
        return html.Div([
            dcc.Input(id='param2', type='text', placeholder='Enter param2', **{'data-id': 'param2'}),
            dcc.Input(id='param3', type='text', placeholder='Enter param3', **{'data-id': 'param3'}),
        ], **{'data-id': 'func2-div'})

    else:
        return html.Div(**{'data-id': 'empty-div'})

def run_function_periodically(func, args):
    while True:
        result = func(*args)
        print(result)  # You can update a UI component instead of printing
        time.sleep(1)

@app.callback(
    Output('output', 'children'),
    Input('start-button', 'n_clicks'),
    State('function-dropdown', 'value'),
    State('param1', 'value'),
    State('param2', 'value'),
    State('param3', 'value')
)
def start_function(n_clicks, selected_function, param1, param2, param3):
    if n_clicks > 0:
        if selected_function == 'func1':
            args = [param1]
            func = func1
        elif selected_function == 'func2':
            args = [param2, param3]
            func = func2
        else:
            raise PreventUpdate
        
        thread = threading.Thread(target=run_function_periodically, args=(func, args))
        thread.daemon = True
        thread.start()
        
        return "Function started"
    else:
        raise PreventUpdate

app.run_server()