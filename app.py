import dash

# install Bootstrap for Dash
# conda install -c conda-forge dash-bootstrap-components
import dash_bootstrap_components as dbc # import the library
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
df = pd.read_csv('https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv')

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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  
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
            html.Div(children='Dash: A web application framework for Python.', style={
                'textAlign': 'center',
                'color': colors['text']
            }),
            dcc.Graph(id="example-graph",
                      figure={"data":[
                              {"x":[1,2,3], "y":[4,2,1], "type": "bar", "name": "DF"},
                              {"x":[1,2,3], "y":[2,4,5], "type": "bar", "name": u'Montréal'}
                              ],
                              'layout': {
                                'plot_bgcolor': colors['background'],
                                'paper_bgcolor': colors['background'],
                                'font': {
                                    'color': colors['text']
                                }
                                }
                    }
            ),
            generate_table(df)
        ])

if __name__ == '__main__':
    app.run_server(port=5050, debug=True) # debug=True to enable hot reload