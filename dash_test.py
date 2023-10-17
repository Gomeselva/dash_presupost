from datetime import timedelta, datetime, date
import os

import dash
from dash import html, dcc 
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

"""Syles"""
url_theme1 =dbc.themes.VAPOR
url_theme2 =dbc.themes.FLATLY
template_theme1 = "vapor"
template_theme2 = "flatly"
card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}


df = pd.read_excel("distribuicao.xlsx")

df_other = df.groupby("Institution")["CY23 Others BUDGET"].sum()
df_IADB_OAS = df.groupby("Institution")["TOTAL BUDGET IADB/OAS"].sum()
df_IADC_OAS = df.groupby("Institution")["TOTAL BUDGET IADC/OAS"].sum()
df_DoD = df.groupby("Institution")["DOD CY23 Cash flow YTD"].sum()

fig = go.Figure(
    data = [
        go.Bar(x=df_IADB_OAS.index, y=df_IADB_OAS.values, name=df_IADB_OAS.name, hovertemplate="%{y:.2s}"),
        go.Bar(x=df_other.index, y=df_other.values, name=df_other.name, hovertemplate="%{y:.2s}"),
        go.Bar(x=df_IADC_OAS.index, y=df_IADC_OAS.values, name=df_IADC_OAS.name, hovertemplate="%{y:.2s}"),
        go.Bar(x=df_DoD.index, y=df_DoD.values, name=df_DoD.name, hovertemplate="%{y:.2s}"),
    ]
)

fig.update_layout(template='plotly_dark')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

institution_list = df["Institution"].value_counts().index.to_list()
category_list = df["Category"].unique()

app.layout = html.Div(
    children = [
        dbc.Row([
            dbc.Col([
                ThemeSwitchAIO(aio_id="theme", themes=[url_theme2, url_theme2]),
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
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=fig)),
                    dbc.Col(dcc.Graph(id="category"))
                ]),
                dbc.Row([
                    dcc.Graph(id="objeto")
                ])
            ], sm=10),
        ])
    ]
)

@app.callback(
    Output("category", "figure"),
    Output("objeto", "figure"),
    Input("check-institution", "value"),
    Input("category-filter", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def render_graph(institution, category, toggle):
    template = template_theme1 if toggle else template_theme2
    filtered_institutions = df[df["Institution"].isin(institution)]
    filtered_category = df[df["Category"]==category]

    fig_category = px.bar(filtered_category, 
                        x=filtered_category["Category"],
                        y=[
                            filtered_category["CY23 Others BUDGET"],
                            filtered_category["TOTAL BUDGET IADB/OAS"],
                            filtered_category["TOTAL BUDGET IADC/OAS"]
                        ],
                        text_auto='.2s')

    fig_objeto = px.bar(df,
                        x=df["Object"],
                        y=[
                            df["CY23 Others BUDGET"],
                            df["TOTAL BUDGET IADB/OAS"],
                            df["TOTAL BUDGET IADC/OAS"]
                        ],
                        text_auto='.2s')

    for figure in (fig_category, fig_objeto):
        figure.update_layout(
            margin=dict(l=0, r=0, t=20, b=20),
            height=500,
            template=template
        )

    return fig_category, fig_objeto

if __name__ == "__main__":
    app.run_server(debug=True)
