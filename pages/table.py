import dash
import pandas as pd
from dash import html, dcc, callback, Input, Output, dash_table
import dash.dash_table.FormatTemplate as FormatTemplate

pd.options.display.float_format = '{:.2f}'.format

dash.register_page(__name__)

df = pd.read_excel("gastos2023_11_01_14_28_03.xlsx")
df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
df.drop(df.columns[0], axis=1, inplace=True)

columns = [
    {
        'id': 'Date',
        'name': 'Date',
        'type': 'datetime'
    },
    {
        'id': 'Instituição',
        'name': 'Instituição',
        'type': 'text'
    },
    {
        'id': 'Category',
        'name': 'Category',
        'type': 'text'
    },
    {
        'id': 'Organ',
        'name': 'Organ',
        'type': 'text'
    },
    {
        'id': 'Account_Number_x',
        'name': 'Account Number',
        'type': 'text'
    },
    {
        'id': 'Object_x',
        'name': 'Object',
        'type': 'text'
    },
    {
        'id': 'Sub-object',
        'name': 'Sub Object',
        'type': 'text'
    },
    {
        'id': 'estimated_budget',
        'name': 'Estimated Budget',
        'type': 'numeric',
        'format': FormatTemplate.money(2)
    },
    {
        'id': 'monthly_occurrence',
        'name': 'Monthly Occurrence',
        'type': 'numeric',
        'format': FormatTemplate.money(2)
    },
    {
        'id': 'until_now_occurrence',
        'name': 'Until Now Occurrence',
        'type': 'numeric',
        'format': FormatTemplate.money(2)
    }
]

layout = html.Div([
    html.H1('Table page'),
    html.Div([
        dash_table.DataTable(
            id='records-table',
            data=df.to_dict('records'),
            columns=columns,
            style_cell={
                'minWidth': '100px',
                'width': '100px',
                'maxWidth': '180px',
                'textAlign': 'left',
                'height': 'auto'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            fill_width=False
        )],
        style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'padding-top': '50px',
            'padding-bottom': '50px',
        }
    )
])
