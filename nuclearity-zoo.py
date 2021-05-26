# Import libraries
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_table
from dash_table.Format import Format, Group
import dash_core_components as dcc
import dash_html_components as html
import re
from dash.dependencies import Input, Output
from skimage import io
#import base64

pd.options.plotting.backend = "plotly"
#pd.set_option("precision", 2)
#data1['shift'] = round(data1['shift'],2)

# Open data
with open('primary_shape_data.pkl', 'rb') as f:
    data1 = pickle.load(f) 
data1 = pd.DataFrame.from_dict(data1)    

# Find all unique nuclearities
nuc_pairs = data1['nuclearity'].unique()
nuc_pairs_dropdown = []
for i in nuc_pairs:
    nuc_pairs_dropdown.append({'label': i, 'value': i})

# Initialize dash layout elements
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Create markdown text for interface
markdown_text1 = '''
 #### Select active component:
'''
markdown_text2 = '''
#### Select inactive component:
'''

markdown_text3 = '''
#### Select nuclearity:
'''

markdown_text10 = '''
#### Select desired formation energy:
'''


actives = {'Pd', 'Pt', 'Rh', 'Ru', 'Ag', 'Ir'}
hosts = {'Zn', 'Al', 'Ga', 'In', 'Cd'}
unique_shapes = sorted(data1['graph_id'].unique())

#encoded_image = base64.b64encode(open('Fig0.png', 'rb').read())
img = io.imread('Fig0.png')
fig = px.imshow(img)

# Create the plotly dash layout
app.layout = html.Div(children=[
    html.H1(children='Nuclearity Zoo'),

    #html.Table(id = 'test output', style={'color': '#6699FF', 'fontSize': 20}),
    #dash_table.DataTable(id='test output', columns=[{"name": i, "id": i} for i in data1.columns]),
    #html.Img(id = 'image', src = img),
    #html.Img(src='data:image/png;base64,{}'.format(encoded_image))
    #dcc.Graph(id = 'image2', figure = fig),
    #html.Figure(id = 'image', children = fig),
    
    # Markdown for the element number checklist
    dcc.Markdown(children=markdown_text1),

    dcc.Checklist(
    id='num-active',
    options=[{'label': i, 'value': i} for i in actives],
    value=list(actives),
    labelStyle={'display': 'inline-block'}
    ),
    
    # Markdown for the element number checklist
    dcc.Markdown(children=markdown_text2),

    dcc.Checklist(
    id='num-inactive',
    options=[{'label': i, 'value': i} for i in hosts],
    value=list(hosts),
    labelStyle={'display': 'inline-block'}
    ),
    
    dcc.Markdown(children=markdown_text3),
    
    # Dropdown bar so the user may select which scaling pair to view
    dcc.Dropdown(
        options=[
            *nuc_pairs_dropdown
        ],
        placeholder="Select nuclearity",
        #value=f'{nuc_pairs[0]}',
        id = 'nuclearity',
    style={"width": "50%"}
    ),
    
    dcc.Markdown(children='#### Testing!'),
        # Range slider with input boxes so the user can choose range of formation energy
    

    dcc.RangeSlider(
        id='my-range-slider',
        min=0,
        max=20,
        step=0.5,
        value=[5, 15]
    ),
    
    

    dcc.Markdown(children='#### Select shape:'),

    dcc.Checklist(
        id = 'shape',
        options=[{'label': i, 'value': i} for i in unique_shapes],
        value=unique_shapes,
        labelStyle={'display': 'inline-block'}
    ),
    
    html.Div(id='output-container-range-slider')
    html.Div(id = 'results found'),
    html.Div(id='table output')
])   


# Other functions

@app.callback(
    Output('shape','options'),
    Input('nuclearity','value'))

def update_element(nuclearity):
    groups = data1.groupby('nuclearity')
    temp = groups.get_group(nuclearity)
    temp = pd.DataFrame(temp)
    shape_list = sorted(temp['graph_id'].unique())
    options = [{'label': i, 'value': i} for i in shape_list]
    return options


# Create dash callback
@app.callback(
    Output('table output', 'children'),
    Output('results found', 'children'),
    Input('num-active', 'value'),
    Input('num-inactive', 'value'),
    Input('nuclearity', 'value'),
    Input('shape', 'value'))
    

# Primary callback function
def update_element(active, inactive, nuclearity,shape):
    data2 = pd.DataFrame()
    pd.set_option("precision", 2)
    groups = data1.groupby(['active_el', 'inactive_el', 'nuclearity','graph_id'])
    for act in active:
        for inact in inactive:
            for sh in shape:
                try:
                    temp = groups.get_group((act, inact, nuclearity,sh))
                    temp = pd.DataFrame(temp)
                    data2 = data2.append(temp)
                except:
                    continue
    #data2 = data2.append(data1.iloc[0:5])
    columns = [{"name": i, "id": i} for i in data1.columns]
    #columns[3]["format"] = Format(precision=2)
    children = dash_table.DataTable(columns=columns,data=data2.to_dict('records'))
    children2 = html.Div(children = str(len(data2))+' results found:')
    return children, children2


if __name__ == '__main__':
    app.run_server(debug=True)
