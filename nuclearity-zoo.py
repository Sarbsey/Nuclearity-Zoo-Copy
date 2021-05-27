import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1(children='Nuclearity Zoo'),
    
    dcc.RangeSlider(
        id='form_energy',
        min=0,
        max=20,
        step=0.5,
        value=[5, 15]
    ),
    html.Div(id='fe_selection')
])


@app.callback(
    dash.dependencies.Output('fe_selection', 'children'),
    [dash.dependencies.Input('form_energy', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
