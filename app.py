import dash
import dash_bootstrap_components as dbc
import os
app_port = 80 # os.environ['APP_PORT']

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
