"""
Created on FRI Dec 30 2022

@author: kristin dahl waters
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px
from datetime import datetime as dt

from datetime import datetime, timedelta
from pandas import DataFrame


#load_figure_template('LUX')

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Boston Fire Analytics: Data Trends"


# INITIALIZE APPLICATION
source_file = '/Users/ksarah/Documents/Source/DataScience/FireReporting/datasets/boston_fire_incidents_2014_dec2022.csv'
property_use_file = '/Users/ksarah/Documents/Source/DataScience/FireReporting/datasets/property-use-code-list.csv'
incident_code_file = '/Users/ksarah/Documents/Source/DataScience/FireReporting/datasets/incident-type-code-list.csv'

fire_data = pd.read_csv(
    source_file, dtype={'zip': 'str', 'alarm_time': 'str', 'neighborhood': 'str'})
inc_code_data = pd.read_csv(incident_code_file)

# Convert timestamps
fire_data['alarm_date'] = pd.to_datetime(
    fire_data['alarm_date'], format="%Y-%m-%d")
fire_data['alarm_time'] = pd.to_datetime(
    fire_data['alarm_time'], format="%H:%M:%S").dt.time

# Data Cleanup
fire_data = fire_data.rename(columns={"incident_type": "code"})
fire_data['neighborhood'] = fire_data['neighborhood'].astype('str')
fire_data['code'] = fire_data['code'].astype('str')
fire_data['month'] = pd.DatetimeIndex(fire_data['alarm_date']).month
fire_data['year'] = pd.DatetimeIndex(fire_data['alarm_date']).year

neighborhood_list = fire_data["neighborhood"].unique()

# Merge incident codes with fire data
fire_data = fire_data.merge(inc_code_data, how='left').drop(columns=['category', 'descript', 'street_prefix', 'xstreet_suffix',
                                                                     'xstreet_prefix', 'xstreet_name', 'xstreet_suffix', 'xstreet_type', 'street_suffix', 'address_2'])

# data = combined.query("grp == '11' and neighborhood == 'CH'")
fire_data.sort_values("alarm_date", inplace=True)

f_data = fire_data.groupby(['year', 'neighborhood', 'code',
                           'alarm_date'], as_index=False).incident_number.count()
f_data.columns = ['year', 'count', 'neighborhood', 'code', 'alarm_date']


# Annual Count
annual_count_data = fire_data.groupby(
    ['year'], as_index=False).incident_number.count()
annual_count_data.columns = ['year', 'count']






# DEFINE LAYOUT

x = np.random.sample(100)
y = np.random.sample(100)
z = np.random.choice(a = ['a','b','c'], size = 100)


df1 = pd.DataFrame({'x': x, 'y':y, 'z':z}, index = range(100))

fig1 = px.scatter(df1, x= x, y = y, color = z)





def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Boston Analytics"),
            html.H3("Welcome to the Boston Fire Analytics Dashboard"),
            html.Div(
                id="intro",
                children="Explore clinic patient volume by time of day, waiting time, and care score. Click on the heatmap to visualize patient experience at different time points.",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Neighborhood"),
            dcc.Dropdown(
                id="neighborhood-filter",
                options=[{"label": i, "value": i} for i in neighborhood_list],
                value=["Charlestown", "Boston"],
                multi=True,
            ),
            html.Br(),
            html.P("Select Time Range"),
            dcc.DatePickerRange(
                id="date-range",
                start_date=dt(2014, 1, 1),
                end_date=dt(2022, 12, 31),
                min_date_allowed=fire_data.alarm_date.min(),
                max_date_allowed=fire_data.alarm_date.max(),
                initial_visible_month=dt(2022, 1, 1),
            ),
            html.Br(),
            html.Br(),
            html.P("Select Incident Type"),
            dcc.Dropdown(
                id="code-filter",
                options=[{"label": i, "value": i} for i in neighborhood_list],
                value=neighborhood_list[:],
                multi=True,
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )



###---------------Create the layout of the app ------------------------


app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="neighborhood-incidents",
                    children=[
                        html.B("Neighborhood Incidents"),
                        html.Hr(),
                        dbc.Col(dcc.Graph(id = 'graph3', config={"displayModeBar": False},))
                        #dcc.Graph(id="graph1"),
                    ],
                ),
                # Patient Volume Heatmap
                html.Div(
                    id="patient_volume_card",
                    children=[
                        html.B("Neighborhood Incidents"),
                        html.Hr(),
                        dbc.Col(dcc.Graph(id = 'graph1', figure = fig1))
                        #dcc.Graph(id="graph1"),
                    ],
                ),
            ],
        ),
    ],
)



@app.callback(
    Output("graph3", "figure"),
    [
        Input("neighborhood-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),

    ],
)
def update_line_chart(neighborhoods, start_date, end_date):
    mask = (
        (fire_data.neighborhood.isin(neighborhoods))
        #& (fire_data.code == incident_code)
        & (fire_data.alarm_date >= start_date)
        & (fire_data.alarm_date <= end_date)
    )
    filtered_data = fire_data.loc[mask, :]

    f_data = filtered_data.groupby(
        ['year', 'neighborhood'], as_index=False).incident_number.count()
    f_data.columns = ['year', 'neighborhood', 'count']

    fig = px.line(f_data[mask],
                  x="year", y="count", color='neighborhood', title="Incidents by Neighborhood")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
