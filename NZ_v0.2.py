#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
with open('primary_shape_data1.pkl', 'rb') as f:
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
actives = {'Pd', 'Pt', 'Rh', 'Ru', 'Ag', 'Ir'}
hosts = {'Zn', 'Al', 'Ga', 'In', 'Cd'}
unique_shapes = sorted(data1['graph_id'].unique())

#encoded_image = base64.b64encode(open('Fig0.png', 'rb').read())
img = io.imread('shape-detection_backup-main/Fig0.png')
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
    #html.Img(src='https://github.com/unnattisharma/shape-detection_backup/blob/c16833aecd47c6da0ec8f3bb3b562c0709105aff/Fig0.png', height='160', width='160'),
    #html.Div(id = 'image', children = fig),
    #html.Img(src=app.get_asset_url('Fig0.png')),
    dcc.Link(id='imagelink', href = 'https://www.cmu.edu/brand/brand-guidelines/images/wordmarksquare-red-600x600.png', children = html.Img(src=app.get_asset_url('Fig0.png'))),#html.H1(children='click here')),
    
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
    
    dcc.Markdown(children='#### Select shape:'),
    
    dcc.Checklist(
        id = 'shape',
        options=[{'label': i, 'value': i} for i in unique_shapes],
        value=unique_shapes,
        labelStyle={'display': 'inline-block'}
    ),
    
    dcc.Markdown(children='#### Formation Energy Range:'),
    
    dcc.RangeSlider(
        id='form_energy',
        min=-0.5,
        max=0,
        step=0.05,
        marks={
            -0.5: '-0.5',
            -0.4: '-0.4',
            -0.3: '-0.3',
            -0.2: '-0.2',
            -0.1: '-0.1',
            0: '0'
        },
        value=[-0.5, 0]
    ),
    
    
    html.Div(id='fe_selection'),
    
    dcc.Markdown('#### Sort by:'),
    
    #Dropdown container for deciding what value to sort by
    dcc.Dropdown(
        id='sorting_keys',
        style={"width": "50%"},
        options=[
            {'label': 'Formation Energy', 'value': 'formation_energy'},
            {'label': 'Graph id', 'value': 'graph_id'},
            {'label': 'Mole Fraction Active Component', 'value': 'active_mol_fr'},
            {'label': 'Shift', 'value': 'shift'}
        ],
        value='shift'
    ),
    html.Div(id='sorting-key-container'),
    
    #Slider for determining if it should be sorted in ascending or descending order 
    dcc.Slider(
        id='ascdesc-slider',
        min=0,
        max=1,
        step=1,
         marks={
        0: 'Descending',
        1: 'Ascending'
    },
        value=1,
    ),
    
    html.Div(id='ascdesc-output-container'), 
    html.Div(id = 'results found'),
    html.Div(id='table output')

])

# Other functions

@app.callback(
    dash.dependencies.Output('fe_selection', 'children'),
    [dash.dependencies.Input('form_energy', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output('shape','options'),
    Input('nuclearity','value'))

def update_element(nuclearity):
    group = data1.groupby('nuclearity')
    temp = group.get_group(nuclearity)
    temp = pd.DataFrame(temp)
    shape_list = sorted(temp['graph_id'].unique())
    options = [{'label': i, 'value': i} for i in shape_list]
    return options

#Sortkey Callback just sets the sortkey to whatever was selected, which should already have 
@app.callback(
    dash.dependencies.Output('sorting-key-container', 'children'),
    [dash.dependencies.Input('sorting_keys', 'value')])
def update_output(value):
    sortkey = value
    return 'You have selected "{}"'.format(sortkey)

#Ascending/Descending Callback
@app.callback(
    dash.dependencies.Output('ascdesc-output-container', 'children'),
    [dash.dependencies.Input('ascdesc-slider', 'value')])
def update_output(value):
    #Determining if it should be in ascending or descending order
    if value == 1:
        upordown = True
        temp = 'Ascending'
    else:
        upordown = False
        temp = 'Descending'
    return 'You have selected "{}"'.format(temp)


# Create dash callback
@app.callback(
    Output('table output', 'children'),
    Output('results found', 'children'),
    Input('num-active', 'value'),
    Input('num-inactive', 'value'),
    Input('nuclearity', 'value'),
    Input('shape', 'value'),
    Input('form_energy', 'value'),
    Input('ascdesc-slider', 'value'),
    Input('sorting_keys', 'value')
)

# Primary callback function
def update_element(active, inactive, nuclearity,shape,energy,upordown,sortkey):
    data2 = pd.DataFrame()
    pd.set_option("precision", 2)
    groups = data1.groupby(['active_el', 'inactive_el', 'nuclearity','graph_id']) #Can move around the order of the keys
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
    data3 = data2[['bulk','miller_index','shift','nuclearity','graph_id','formation_energy','active_mol_fr']]
    data3 = data3[data3['formation_energy']>=energy[0]]
    data3 = data3[data3['formation_energy']<=energy[1]]
    columns = [{"name": i, "id": i} for i in data3.columns]
    data3 = data3.sort_values(by=[sortkey], axis=0, ascending=upordown, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)

    #columns[3]["format"] = Format(precision=2)
    children = dash_table.DataTable(columns=columns,data=data3.to_dict('records'))
    children2 = html.Div(children = str(len(data3))+' results found:')
    return children, children2


if __name__ == '__main__':
    app.run_server()


# In[ ]:




