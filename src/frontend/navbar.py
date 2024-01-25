import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(f"Patient {i}", href=f"/live/{i}") for i in range(1,7)
            ],
            nav=True,
            in_navbar=True,
            label="Live sensor measurements",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(f"Patient {i}", href=f"/history/{i}") for i in range(1,7)
            ],
            nav=True,
            in_navbar=True,
            label="Last anomaly sensor measurements",
        ),
    ],
    brand="Foot Sensor App",
    brand_href="/",
    color="#060c85",
    dark=True,
    fluid=True,
    links_left=True,
    sticky='Top'
)