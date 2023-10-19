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
load_figure_template([base_fig_theme, base_fig_theme + "_dark"])

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

institution_list = df["Institution"].value_counts().index.to_list()
category_list = df["Category"].unique()

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
                    html.Br(),
                    dcc.RadioItems(
                        category_list,
                        id="category-filter",
                        value=category_list[0],
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
                                "height": 100,
                                "margin-left": "-10px"
                            }
                        )
                    ])
                ],
                style={
                    "height": "90vh",
                    "margin": "10px",
                    "padding": "10px"
                })
            ], sm=2),
            dbc.Col([
                html.Div(children=[
                    dcc.Graph(
                        id="institution-fig",
                        config={"displayModeBar": False},
                        style={"display": "inline-block"}
                    ),
                    dcc.Graph(
                        id="category",
                        config={"displayModeBar": False},
                        style={"display": "inline-block"}
                    )
                ]),
                dbc.Row([
                    dcc.Graph(
                        id="objeto",
                        config={"displayModeBar": False},
                    )
                ])
            ], sm=10),
        ])
    ]
)

@app.callback(
    Output("institution-fig", "figure"),
    Output("category", "figure"),
    Output("objeto", "figure"),
    Input("check-institution", "value"),
    Input("category-filter", "value"),
    Input("color-mode-switch", "value"),
)

def render_graph(institution, category, switch_on):
    template = pio.templates[base_fig_theme] if switch_on else pio.templates[base_fig_theme + "_dark"]

    filtered_category = df[df["Category"] == category]
    institution_filter = df["Institution"].isin(institution)

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
        template=template
    )

    fig_category = px.histogram(
        filtered_category, 
        x=filtered_category["Category"],
        y=[
            filtered_category["CY23 Others BUDGET"],
            filtered_category["TOTAL BUDGET IADB/OAS"],
            filtered_category["TOTAL BUDGET IADC/OAS"]
        ],
        text_auto='.2s',
        template=template
    )

    fig_objeto = px.histogram(
        df,
        x=df["Object"],
        y=[
            df["CY23 Others BUDGET"],
            df["TOTAL BUDGET IADB/OAS"],
            df["TOTAL BUDGET IADC/OAS"]
        ],
        text_auto='.2s',
        template=template
    )

    for figure in(fig_institution, fig_category, fig_objeto):
        figure.update_layout(
            margin=dict(l=0, r=0, t=20, b=20),
            height=400,
            title_x=0.5
        )

    return fig_institution, fig_category, fig_objeto

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
