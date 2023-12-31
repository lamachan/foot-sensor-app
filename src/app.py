import dash
from dash import html

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div([
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)