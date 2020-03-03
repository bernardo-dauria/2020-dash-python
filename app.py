import dash
import dash_html_components as html

app = dash.Dash(__name__)
app.title = 'My First Dash App'

app.layout = html.H1('Hello Dash')

if __name__ == '__main__':
    app.run_server(debug=True) # debug=True to enable hot reload