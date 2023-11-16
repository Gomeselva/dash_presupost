import dash
from dash import html, Dash
import dash_bootstrap_components as dbc

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc_css])

app.layout = html.Div(
    children = [
        dash.page_container,
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
    ##
# if __name__ == "__main__":

#     app.run_server(debug=False, port=8080, host="0.0.0.0")
