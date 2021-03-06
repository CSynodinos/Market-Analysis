from __future__ import annotations

import os, sys
from typing import Any
SCRIPT_DIR = os.path.dirname(os.path.abspath("__file__"))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from lib.db_utils import SQLite_Query
import dash
from dash import dcc, html
import pandas as pd
import webbrowser
from threading import Timer

##http://localhost:8050

def __dashboard_create(df: pd.DataFrame, asset: str, asset_type: str, next_day: int | float,
                    volatility: str) -> dash.Dash:

    """Create a one graph dashboard using dash.

    Args:
        * `df` (pd.DataFrame): DataFrame with the dashboard data.
        * `asset` (str): Asset name.
        * `asset_type` (str): Type of asset.
        * `next_day` (int | float): Next day prediction value.
        * `volatility` (str): Volatility percentage value.

    Returns:
        Dash: Instance of the dash web application.
    """

    external_stylesheets = [
        {
            "href": "https://fonts.googleapis.com/css2?"
                    "family=Lato:wght@400;700&display=swap",
            "rel": "stylesheet",
        },
    ]
    app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
    app.title = "Market Analysis using ML!!!"
    app.layout = html.Div(
        children = [
            html.Div(
                children = [
                    html.P(children="📈", className = "header-emoji"),
                    html.H1(
                        children="Market Analytics", className = "header-title"
                    ),
                    html.P(
                        children = f"Analyze {asset_type} prices using a Recursive Neural Network. "
                        f"Predict the price of the {asset_type} for the next day from the specified date.",
                        className="header-description",
                    ),
                ],
                className = "header",
            ),
            html.Div(
                children = [
                    html.Div(
                        children = dcc.Graph(
                            id = "price-chart",
                            config = dict({ 'displayModeBar': True,
                                        'scrollZoom': True,
                                        'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'scrollZoom',
                                        'drawclosedpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                        ]
                                    }
                                ),
                            figure = {
                                "data": [
                                    {
                                        "x": df.iloc[:, 1],
                                        "y": df.iloc[:, 2],
                                        "type": "lines",
                                        "line": dict(color = 'green'),
                                        "name": f"{df.columns[2]}",
                                        "hovertemplate": "$%{y:.2f}"
                                                        "<extra></extra>",
                                        },
                                    {
                                        "x": df.iloc[:, 1],
                                        "y": df.iloc[:, 3],
                                        "type": "lines",
                                        "name": f"{df.columns[3]}",
                                        "line": dict(color = 'magenta'),
                                        "hovertemplate": "$%{y:.2f}"
                                                        "<extra></extra>",
                                        },
                                    ],
                                "layout": {
                                    "title": {
                                        "text": f"{asset} {asset_type} Price Prediction",
                                        "x": 0.35,
                                        "xanchor": "left",
                                    },
                                    "xaxis": {"fixedrange": True},
                                    "yaxis": {
                                        "tickprefix": "$",
                                        "fixedrange": True,
                                    },
                                },
                            },
                        ),
                        className = "card",
                    ),
                ],
                className="wrapper",
            ),
        html.Div(
        children = [
            html.Div(
                children = [
                    html.Span(
                        children=dcc.Markdown("_**Description**_: The prediction for the price of the " 
                                            f"asset on the next day (Previous date: {df['Dates'].iloc[-1]}) "
                                            f"is: **${next_day}**. The mean volatility of "
                                            f"the asset is **{volatility}**%.", className = "legend-title")
                    ),
                    html.Span(
                        className = "legend-description",
                    ),
                ],
                className = "Legend",
                ),
            ])
        ]
    )
    return app

def dashboard_launch(db: str, table: str, fin_asset: str, asset_type: str, 
                nxt_day: float | int, volatility: str, port: int) -> Any:

    """Launch a dash dashboard.

    Args:
        * `db` (str): Name of database.
        * `table` (str): Table with asset data.
        * `fin_asset` (str): Name of asset.
        * `asset_type` (str): Type of asset e.g. crypto, stock.
        * `nxt_day` (float | int): Next day price prediction.
        * `volatility` (str): Volatility of asset.
        * `port` (int, optional): Port for server.

    Returns:
        Launches an instance of the app.
    """

    df = SQLite_Query(database = db, table = table)[0]
    app = __dashboard_create(df = df, asset = fin_asset, asset_type = asset_type, next_day = nxt_day,
                        volatility = volatility)
    Timer(1, webbrowser.open_new, args = (f"http://localhost:{port}",)).start()
    return app.run(port = port)