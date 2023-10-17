"""módulos internos"""
from datetime import timedelta, datetime, date
import os
"""módulos de terceiros"""
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


# df_other = df.loc[df["CY23 Others BUDGET"]>0, ["Instituição", "CY23 Others BUDGET"]]
# df_IADB_OAS = df.loc[df["TOTAL BUDGET IADB/OAS"]>0, ["Instituição", "TOTAL BUDGET IADB/OAS"]]
# df_IADC_OAS = df.loc[df["TOTAL BUDGET IADC/OAS"]>0, ["Instituição", "TOTAL BUDGET IADC/OAS"]]
# df_DoD = df.loc[df["DOD CY23 Cash flow YTD"]>0, ["Instituição", "DOD CY23 Cash flow YTD"]]


df_other = df.groupby("Instituição")["CY23 Others BUDGET"].sum()
df_IADB_OAS = df.groupby("Instituição")["TOTAL BUDGET IADB/OAS"].sum()
df_IADC_OAS = df.groupby("Instituição")["TOTAL BUDGET IADC/OAS"].sum()
df_DoD = df.groupby("Instituição")["DOD CY23 Cash flow YTD"].sum()

# dic_1={"IADB":{"other":111387.11, "OAS":652080.38, "DoD": 0.0}, "IADC":{"other":0.0, "OAS":218500.0, "DoD":1898097.48}}

# df_DoD.index()

# fig = go.Figure(
#     data= [
#         go.Bar(x= dic_1.keys(), y=dic_1.values()),
      
#     ]
# )


fig = go.Figure(
    data= [
        go.Bar(x= df_IADB_OAS.index, y=df_IADB_OAS.values),
        go.Bar(x= df_other.index, y=df_other.values),
        go.Bar(x= df_IADC_OAS.index, y=df_IADC_OAS.values),
        go.Bar(x= df_DoD.index, y=df_DoD.values)
    ]
)





# fig_fundos = px.bar(df, x=df["Instituição"], y=[df["CY23 Others BUDGET"].sum(), df["TOTAL BUDGET IADB/OAS"].sum(), df["TOTAL BUDGET IADC/OAS"].sum()])



#=======================  layout ==================#

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
                    children=[
                    dbc.Row([
                    dbc.Col([
                        ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                        dbc.Card([
                        html.H2("Financial Report", style = {"font-family": "Voltair", "font-size": "50px", "color": "orange"},id="h1"), html.Br(),
                        html.H5("Instituição"),
                        dcc.Checklist(df["Instituição"].value_counts().index.to_list(),
                        value=df["Instituição"].value_counts().index.to_list(), id="Check-instituição", inputStyle={"margin-right": "5px", "margin-left": "20px"}),
                        html.H5("Categories", style = {"margin-top": "30px"}), html.Br(),
                        dcc.RadioItems(df["Category"].unique(), value=df["Category"].unique()[0], id="Category", inputStyle={"margin-right": "5px", "margin-left": "20px"}, inline=True), html.Br(),
                        dbc.CardGroup([
                            dbc.Card([
                                html.Legend("Total Previsto"),
                                html.H5("R$ 5,000.80", id="saldo-p", style={})
                            ], style={"pading-left": "10px", "padin-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa university", style=card_icon), color="warming",
                                style={"maxwidth": 50, "heigth": 100, "margin-left": "-10px"}
                            )
                    ]), html.Br(),
                            dbc.CardGroup([
                                dbc.Card([
                                    html.Legend("Total Gasto"),
                                    html.H5("R$ 14,000.80", id="saldo-t", style={})
                                ], style={"pading-left": "10px", "padin-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa university", style=card_icon), color="warming",
                                style={"maxwidth": 50, "heigth": 100, "margin-left": "-10px"}
                                    )
                            ])], style={"height": "90vh", "margin": "10px ", "padding" : "10px" })
                        ], sm=2),
                        dbc.Col([
                        dbc.Row([
                            dbc.Col ([dcc.Graph(figure=fig)]),
                            dbc.Col([dcc.Graph(id="category")])
                            ]),
                        dbc.Row([dcc.Graph(id="objeto")])
                            ], sm=10
                        )    
                    ])
                    ])

#=======================  Callbacks ==================#
@app.callback(
            Output("category", "figure"),
            Output("objeto", "figure"),
            Input("Check-instituição", "value"),
            Input("Category", "value"),
            Input(ThemeSwitchAIO.ids.switch("theme"), "value")
            )
def render_graph(instituição, categoria, toggle):
    template = template_theme1 if toggle else template_theme2
    df_1 = df[df["Instituição"].isin(instituição)]
    df_2 = df_1[df_1["Category"].isin(categoria)]
    fig_category = px.bar(df_2, x=df_2["Category"], y=[df_2["CY23 Others BUDGET"], df_2["TOTAL BUDGET IADB/OAS"], df_2["TOTAL BUDGET IADC/OAS"], df[""]])
    fig_objeto = px.bar(df, x=df["Object"], y=[df["CY23 Others BUDGET"], df["TOTAL BUDGET IADB/OAS"], df["TOTAL BUDGET IADC/OAS"]])
    
    
    for fig in(fig_category, fig_objeto):
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=300, template=template)

    return fig_category, fig_objeto

# @app.callback(
#             Output("inflação", "figure"),
#             Output("novo-2", "figure"),
#             Input(ThemeSwitchAIO.ids.switch("theme"), "value")
#             )
# def inflacao(toggle):
#     template = template_theme1 if toggle else template_theme2
#     month_sum = pd.DataFrame(df.loc[df["Category"] == "Gastos Fixos"].groupby("month")["Debit"].sum())
#     month_sum.reset_index(inplace=True)
#     dict_1 = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

#     for k,v in dict_1.items():
#         month_sum.loc[month_sum["month"] == k, "ordem"] = v
    
#     month_sum.set_index("ordem", inplace=True)
#     month_sum.sort_index(inplace=True)
   
#     lista_4 = [x for x in calculo_inflacao(month_sum)]
#     month_sum["Inflação"] = lista_4
#     fig_inflacao = px.bar(month_sum, x=month_sum["month"], y=month_sum["Inflação"])
#     fig_inflacao.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=300, template=template)
#     fig_novo = fig_inflacao
#     return fig_inflacao, fig_novo



#=======================  Run  Server ==================#
if __name__ == "__main__":
    app.run_server(debug=True)

# if __name__ == "__main__":
#     app.run_server(debug=False, port=8080, host="0.0.0.0")



    
    



    






            
            


