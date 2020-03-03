import dash
import logging

# install Bootstrap for Dash
# conda install -c conda-forge dash-bootstrap-components
import dash_bootstrap_components as dbc # import the library
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import pandas as pd
db_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
db = pd.read_csv(db_url)
db_vore = db['vore'].dropna().sort_values().unique()
opt_vore = [{'label': x + 'vore', 'value': x} for x in db_vore]

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr(
            [html.Td(row[col]) for col in row.index.values]
        ) for index, row in dataframe.head(max_rows).iterrows()]
    )


#load the app with the Bootstrap css theme
#external_stylesheets = [dbc.themes.BOOTSTRAP]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  
app.title = 'My First Dash App'

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

markdown_text = '''
#### Some references

[Dash Core Components](https://dash.plot.ly/dash-core-components)  
[Dash HTML Components](https://dash.plot.ly/dash-html-components)  
[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/l/components)  

'''

app.layout = html.Div(style={"backgroundColor": colors['background'], 'color': colors['text']}, children=[
            html.H1('Hello Dash', style={
                    'textAlig':"center",
                    'color': colors['text']
                    }),
            dcc.Markdown(markdown_text),
            
            html.Div(id='my-div',
             style={
                 'background' : 'yellow',
                 'color' : 'blue'
             }),
    
            dcc.Graph(id='my-graph'),
            dcc.Graph(id='my-box-plot'),
            
            # generate_table(db)
            
            html.Div([
                html.Label('Dropdown'),
                dcc.Dropdown(
                        id='my-dropdown',
                        options=opt_vore,
                        value=db_vore[0]
                ),
                
                html.Label('Multi-Select Dropdown'),
                dcc.Dropdown(
                    id='my-multi-dropdown',
                    options=opt_vore,
                    value=db_vore[0],
                    multi=True
                ),
            
                html.Label('Radio Items'),
                dcc.RadioItems(
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': u'Montréal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='MTL'
                ),
            
                html.Label('Checkboxes'),
                dcc.Checklist(
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': u'Montréal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value=['MTL', 'SF']
                ),
            
                html.Label('Text Input'),
                dcc.Input(value='MTL', type='text'),
            
                html.Div([
                    html.Label('Slider'),
                    html.Div(
                        dcc.RangeSlider(
                            id='my-slider',
                            step=0.1,
                            min=min(db['sleep_total']),
                            max=max(db['sleep_total'])
                        ),
                        style={
                            'width': '60%',
                            'display': 'inline-block',
                            'paddingLeft': '10%',
                            'paddingRight': '10%'
                        }
                    ),
                    html.Button('Update filter', id='my-button')
                ],
                    style={
                        'marginTop': '5%',
                        'marginBottom': '5%'
                    }
                ),
            ], style={'columnCount': 2})    
        ])
                
@app.callback(
    Output('my-div', 'children'),
    [Input('my-dropdown', 'value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

@app.callback(
    [Output('my-graph', 'figure'),
     Output('my-box-plot', 'figure'),],
    [Input('my-multi-dropdown', 'value'), 
     Input('my-button', 'n_clicks')],
    [State('my-slider', 'value')]
)
def update_output_graph(input_value, n_clicks, slider_range):
    if (slider_range and len(slider_range) == 2):
        l, h = slider_range
    else :
        l, h = min(db['sleep_total']), max(db['sleep_total']);
    df = db[db['sleep_total'].between(l,h)]
    return  {
                'data': [
                    go.Scatter(
                        x=df[df['vore'] == i]['bodywt'] if i in input_value else [],
                        y=df[df['vore'] == i]['sleep_total'] if i in input_value else [],
                        text=df[df['vore'] == i]['name'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in db_vore
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'Body weight (kg)'},
                    yaxis={'title': 'Total daily sleep time (hr)'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            },{
                'data': [ go.Box(
                            y= df[df['vore'] == i]['sleep_total'],
                            name= i + 'vore'
                        ) if i in input_value else {}
                          for i in db_vore ]
            }
                
@app.callback(
    [Output('my-slider', 'min'), 
     Output('my-slider', 'max'), 
     Output('my-slider', 'value'), 
     Output('my-slider', 'marks')],
    [Input('my-multi-dropdown', 'value')]
)
def update_slider(input_value):
    def round(x):
        return int(x) if x % 0.1 < 0.1 else x
    
    s = pd.Series(input_value, name='vore')
    data = db[db.vore.isin(s)]['sleep_total'] 
    
    min = round(data.min())
    max = round(data.max())
    mean = round(data.mean())
    low = round((min + mean)/2)
    high = round((max + mean) / 2)
    marks = {min: {'label': str(min), 'style': {'color': '#77b0b1'}},
             max: {'label': str(max), 'style': {'color': '#77b0b1'}}}
    return min, max,  [low, high], marks 

if __name__ == '__main__':
    # app.server.logger.setLevel(logging.DEBUG)
    # app.server.logger.debug("debug-message")
    app.run_server(port=5057, debug=True) # debug=True to enable hot reload