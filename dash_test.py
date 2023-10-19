from datetime import timedelta, datetime, date
import os

from dash import html, dcc, Dash, Input, Output, Patch, callback, clientside_callback 
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

base_fig_theme = "bootstrap"
load_figure_template([base_fig_theme + "_dark", base_fig_theme])

df = pd.read_excel("distribuicao.xlsx")

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc_css])

color_mode_switch = html.Span([
    dbc.Label(className="fa fa-moon", html_for="switch"),
    dbc.Switch(id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
    dbc.Label(className="fa fa-sun", html_for="switch"),
])

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

institution_list = df["Institution"].unique()
category_list = df["Category"].unique()
object_list = df["Object"].unique()

app.layout = html.Div(
    children = [
        dbc.Row([
            dbc.Col([
                color_mode_switch,
                dbc.Card([
                    html.H2("Financial Report", id="h1", style = {
                        # "font-family": "Helvetica", 
                        "font-size": "50px",
                        "color": "orange"
                    }),
                    html.Br(),
                    html.H5("Institution"),
                    dcc.Checklist(
                        institution_list,
                        id="check-institution",
                        value=institution_list,
                        inputStyle={
                            "margin-right": "5px",
                            "margin-left": "20px"
                        }
                    ),
                    html.H5("Category", style={"margin-top": "30px"}),
                    dcc.Checklist(
                        category_list,
                        id="category-filter",
                        value=category_list,
                        inputStyle={
                            "margin-right": "5px",
                            "margin-left": "20px"
                        },
                        inline=True
                    ),
                    html.Br(),
                    html.H5("Object", style={"margin-top": "30px"}),
                    dcc.Checklist(
                        object_list,
                        id="object-filter",
                        value=object_list,
                        inputStyle={
                            "margin-right": "5px",
                            "margin-left": "20px"
                        },
                        inline=True
                    ),
                    html.Br(),
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend("Total Previsto"),
                            html.H5("R$ 5,000.80", id="saldo-previsto")
                        ],
                        style = {
                            "padding-left": "10px",
                            "padding-top":"10px"
                        }),
                        dbc.Card(
                            html.Div(className="fa fa university", style=card_icon),
                            color="warming",
                            style={
                                "maxwidth": 50,
                                "height": 100,
                                "margin-left": "-10px"
                            }
                        )
                    ]),
                    html.Br(),
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend("Total Gasto"),
                            html.H5("R$ 14,000.80", id="salto-total")
                        ],
                        style={
                            "padding-left": "10px",
                            "padding-top": "10px"
                        }),
                        dbc.Card(
                            html.Div(className="fa fa university", style=card_icon),
                            color="warming",
                            style={
                                "maxwidth": 50,
                                # "height": 100,
                                "margin-left": "-10px"
                            }
                        )
                    ])
                ],
                style={
                    "height": "100vh",
                    "margin": "10px",
                    "padding": "10px"
                })
            ], width=2),
            dbc.Col([
                # html.Div(children=[
                #     dcc.Graph(
                #         id="institution-fig",
                #         config={"displayModeBar": False},
                #         style={"display": "inline-block"}
                #     ),
                #     dcc.Graph(
                #         id="category",
                #         config={"displayModeBar": False},
                #         style={"display": "inline-block"}
                #     )
                # ]),
                dbc.Row([
                    dcc.Graph(
                        id="institution-fig",
                        config={"displayModeBar": False},
                    )
                ]),
                dbc.Row([
                    dcc.Graph(
                        id="category",
                        config={"displayModeBar": False},
                    )
                ]),
                dbc.Row([
                    dcc.Graph(
                        id="objeto",
                        config={"displayModeBar": False},
                    )
                ])
            ], width=10),
        ])
    ]
)

@callback(
    Output("institution-fig", "figure"),
    Output("category", "figure"),
    Output("objeto", "figure"),
    Input("check-institution", "value"),
    Input("category-filter", "value"),
    Input("object-filter", "value"),
)

def render_graph(institution, category, obj):
    institution_filter = df["Institution"].isin(institution)
    category_filter = df["Category"].isin(category)
    object_filter = df["Object"].isin(obj)

    fig_institution = px.histogram(
        df[institution_filter],
        x="Institution",
        y=[
            "CY23 Others BUDGET",
            "TOTAL BUDGET IADB/OAS",
            "TOTAL BUDGET IADC/OAS",
            "DOD CY23 Cash flow YTD"
        ],
        barmode="group",
        text_auto='.2s',
    )

    fig_category = px.histogram(
        df[category_filter],
        y="Category",
        x=[
            "CY23 Others BUDGET",
            "TOTAL BUDGET IADB/OAS",
            "TOTAL BUDGET IADC/OAS",
        ],
        text_auto='.2s',
    )

    fig_objeto = px.histogram(
        df[object_filter],
        y="Object",
        x=[
            "CY23 Others BUDGET",
            "TOTAL BUDGET IADB/OAS",
            "TOTAL BUDGET IADC/OAS",
        ],
        text_auto='.2s',
    )

    return fig_institution, fig_category, fig_objeto

@callback(
    Output("institution-fig", "figure", allow_duplicate=True),
    Output("category", "figure", allow_duplicate=True),
    Output("objeto", "figure", allow_duplicate=True),
    Input("color-mode-switch", "value"),
    prevent_initial_call=True
)

def update_theme(switch_on):
    template = pio.templates[base_fig_theme] if switch_on else pio.templates[base_fig_theme + "_dark"]

    patched_institution_fig = Patch()
    patched_category_fig = Patch()
    patched_objeto_fig = Patch()

    patched_institution_fig["layout"]["template"] = template
    patched_category_fig["layout"]["template"] = template
    patched_objeto_fig["layout"]["template"] = template

    return patched_institution_fig, patched_category_fig,patched_objeto_fig

clientside_callback(
    """
    switchOn => {       
       switchOn
         ? document.documentElement.setAttribute('data-bs-theme', 'light')
         : document.documentElement.setAttribute('data-bs-theme', 'dark')
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

if __name__ == "__main__":
    app.run_server(debug=True)
