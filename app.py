import dash

# install Bootstrap for Dash
# conda install -c conda-forge dash-bootstrap-components
import dash_bootstrap_components as dbc # import the library
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd
df_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
df = pd.read_csv(df_url)
df_vore = df['vore'].dropna().sort_values().unique()
opt_vore = [{'label': x + 'vore', 'value': x} for x in df_vore]

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
            
            # generate_table(df)
            
            html.Div([
                html.Label('Dropdown'),
                dcc.Dropdown(
                        id='my-dropdown',
                        options=opt_vore,
                        value=df_vore[0]
                ),
                
                html.Label('Multi-Select Dropdown'),
                dcc.Dropdown(
                    id='my-multi-dropdown',
                    options=opt_vore,
                    value=df_vore[0],
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
            
                html.Label('Slider'),
                dcc.Slider(
                    min=0,
                    max=9,
                    marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                    value=5,
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
    [Input('my-multi-dropdown', 'value')]
)
def update_output_graph(input_value):
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
                    ) for i in df_vore
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
                          for i in df_vore ]
            }
if __name__ == '__main__':
    app.run_server(port=5055, debug=True) # debug=True to enable hot reload