# Import necessary libraries
import dash
from dash import html
import dash_bootstrap_components as dbc

# Register pages
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[
    dbc.themes.BOOTSTRAP, 
    "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"])
server = app.server

# Define the layout of the app
app.layout = dbc.Container([
    html.H2("Fußball-Dashboard", style={"color": "white"}),

    # Navigation bar with links to all registered pages
    dbc.Nav([
        dbc.NavLink(page["name"], href=page["path"], active="exact")
        for page in dash.page_registry.values()
    ], pills=True),

    dash.page_container
], fluid=True, style={'backgroundColor': 'black'})

if __name__ == '__main__':
    app.run(debug=True, port=8056)