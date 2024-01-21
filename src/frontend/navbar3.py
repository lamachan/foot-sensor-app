import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Patient 1", href="/history/1")),
        dbc.NavItem(dbc.NavLink("Patient 2", href="/history/2")),
        dbc.NavItem(dbc.NavLink("Patient 3", href="/history/3")),
        dbc.NavItem(dbc.NavLink("Patient 4", href="/history/4")),
        dbc.NavItem(dbc.NavLink("Patient 5", href="/history/5")),
        dbc.NavItem(dbc.NavLink("Patient 6", href="/history/6")),
    ],
    color="primary",
    dark=True,
    fluid=True,
    links_left=True,
    sticky='Top'
)