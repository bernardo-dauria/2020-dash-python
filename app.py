import dash

# install Bootstrap for Dash
# conda install -c conda-forge dash-bootstrap-components
import dash_bootstrap_components as dbc # import the library
import dash_core_components as dcc
import dash_html_components as html


#load the app with the Bootstrap css theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  
app.title = 'My First Dash App'

markdown_text = '''
#### Some references

[Dash Core Components](https://dash.plot.ly/dash-core-components)  
[Dash HTML Components](https://dash.plot.ly/dash-html-components)  
[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/l/components)  

'''

app.layout = html.Div([
            html.H1('Hello Dash'),
            dcc.Markdown(markdown_text),
            dcc.Graph(id="example-graph",
                      figure={"data":[
                              {"x":[1,2,3], "y":[4,2,1], "type": "bar", "name": "DF"},
                              {"x":[1,2,3], "y":[2,4,5], "type": "bar", "name": u'Montréal'}
                              ]
                      }
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True) # debug=True to enable hot reload