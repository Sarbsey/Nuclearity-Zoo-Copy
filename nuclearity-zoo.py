import dash_core_components as dcc

app.layout = html.Div(children=[
    html.H1('My Dash App'),
    html.Div(
        [
            html.Label('From 2007 to 2017', id='time-range-label'),
            dcc.RangeSlider(
                id='year_slider',
                min=1991,
                max=2017,
                value=[2007, 2017]
            ),
        ],
        style={'margin-top': '20'}
    ), 
    html.Hr(),
    dcc.Graph(id='my-graph')
])
