import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Live sensor measurements", href="/live")),
        dbc.NavItem(dbc.NavLink("Last anomaly sensor measurements", href="/history")),
    ],
    brand="Foot Sensor App",
    brand_href="/",
    color="#023069",
    dark=True,
    fluid=True,
    links_left=True,
    sticky='Top'
)