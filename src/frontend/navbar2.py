import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Patient 1", href="/live/1")),
        dbc.NavItem(dbc.NavLink("Patient 2", href="/live/2")),
        dbc.NavItem(dbc.NavLink("Patient 3", href="/live/3")),
        dbc.NavItem(dbc.NavLink("Patient 4", href="/live/4")),
        dbc.NavItem(dbc.NavLink("Patient 5", href="/live/5")),
        dbc.NavItem(dbc.NavLink("Patient 6", href="/live/6")),
    ],
    color="primary",
    dark=True,
    fluid=True,
    links_left=True,
    sticky='Top'
)