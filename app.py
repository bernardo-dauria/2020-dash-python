import dash
import dash_html_components as html

# install Bootstrap for Dash
# conda install -c conda-forge dash-bootstrap-components
import dash_bootstrap_components as dbc # import the library


#load the app with the Bootstrap css theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  
app.title = 'My First Dash App'

app.layout = html.H1('Hello Dash')

if __name__ == '__main__':
    app.run_server(debug=True) # debug=True to enable hot reload