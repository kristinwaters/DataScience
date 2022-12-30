"""
Created on FRI Dec 30 2022

@author: kristin dahl waters
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

from datetime import datetime, timedelta
from pandas import DataFrame

# INITIALIZE APPLICATION
source_file = '../datasets/boston_fire_incidents_2014_dec2022.csv'
incident_code_file = '../datasets/incident-type-code-list.csv'

fire_data = pd.read_csv(
    source_file, dtype={'zip': 'str', 'alarm_time': 'str', 'neighborhood': 'str'})
code_data = pd.read_csv(incident_code_file)

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

# Merge codes with fire data
fire_data = fire_data.merge(code_data, how='left').drop(columns=['category', 'descript', 'street_prefix', 'xstreet_suffix',
                                                                 'xstreet_prefix', 'xstreet_name', 'xstreet_suffix', 'xstreet_type', 'street_suffix', 'address_2', 'category'])

# data = combined.query("grp == '11' and neighborhood == 'CH'")
fire_data.sort_values("alarm_date", inplace=True)

f_data = fire_data.groupby(['year', 'neighborhood', 'code',
                           'alarm_date'], as_index=False).incident_number.count()
f_data.columns = ['year', 'count', 'neighborhood', 'code', 'alarm_date']

# Extract incidents in 2022 only
f_data22 = fire_data.query('"2022-01-01" <= alarm_date <= "2022-12-31"')
f_data22['month'] = pd.DatetimeIndex(f_data22['alarm_date']).month
f_data22 = f_data22.groupby(['month'], as_index=False).incident_number.count()
f_data22.columns = ['month', 'count']

# Annual Count
annual_count_data = fire_data.groupby(['year'], as_index=False).incident_number.count()
annual_count_data.columns = ['year', 'count']


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Boston Fire Analytics: Data Trends"


# DEFINE LAYOUT

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🔥", className="header-emoji"),
                html.H1(
                    children="Boston Fire Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the incidents responded to by Boston Fire"
                    " and the type of incidents"
                    " between 2014 and 2022",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Neighborhood",
                                 className="menu-title"),
                        dcc.Dropdown(
                            id="neighborhood-filter",
                            options=[
                                {"label": neighborhood, "value": neighborhood}
                                for neighborhood in np.sort(fire_data.neighborhood.unique())
                            ],
                            value="Charlestown",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Code", className="menu-title"),
                        dcc.Dropdown(
                            id="code-filter",
                            options=[
                                {"label": incident_code, "value": incident_code}
                                for incident_code in np.sort(fire_data.code.unique())
                            ],
                            value="100",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=fire_data.alarm_date.min(),
                            max_date_allowed=fire_data.alarm_date.max(),
                            start_date=fire_data.alarm_date.min(),
                            end_date=fire_data.alarm_date.max(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="annual-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart",
                                             "figure"), Output("annual-chart", "figure")],
    [
        Input("neighborhood-filter", "value"),
        Input("code-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(neighborhood, incident_code, start_date, end_date):
    mask = (
        (fire_data.neighborhood == neighborhood)
        & (fire_data.code == incident_code)
        & (fire_data.alarm_date >= start_date)
        & (fire_data.alarm_date <= end_date)
    )
    filtered_data = fire_data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": f_data22["month"],
                "y": f_data22["count"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}"
                "<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Incidents in 2022",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {
                "fixedrange": True,
            },
            "colorway": ["#17B897"],
        },
    }
    filtered_annual_count_data = filtered_data.groupby(['year'], as_index=False).incident_number.count()
    filtered_annual_count_data.columns = ['year', 'count']

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_annual_count_data["year"],
                # f_data = fire_data.groupby(['year', 'neighborhood', 'code', 'alarm_date'], as_index=False).incident_number.count()
                "y": filtered_annual_count_data["count"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}"
                "<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Filtered Incidents: " + neighborhood,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    annual_chart_figure = {
        "data": [
            {
                "x": annual_count_data["year"],
                "y": annual_count_data["count"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}"
                "<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "All Incidents",
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure, annual_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
