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


@app.callback(
    output=Output('my-graph', 'figure'),
    inputs=[Input('year_slider', 'value')]
    )
def _update_graph(year_range):
    date_start = '{}-01-01'.format(year_range[0])
    date_end = '{}-12-31'.format(year_range[1])
    
    @app.callback(
    output=Output('time-range-label', 'children'),
    inputs=[Input('year_slider', 'value')]
    )
def _update_time_range_label(year_range):
    return 'From {} to {}'.format(year_range[0], year_range[1])
