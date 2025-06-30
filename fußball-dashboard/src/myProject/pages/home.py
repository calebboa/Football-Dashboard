# Import necessary libraries
import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import random

# Liste der Fußball-Fakten
facts = [
    "Cristiano Ronaldo ist der erste Spieler, der in fünf Weltmeisterschaften getroffen hat.",
    "Der höchste WM-Sieg war 10:1 – Ungarn gegen El Salvador in 1982.",
    "Lionel Messi hat über 100 Tore für die argentinische Nationalmannschaft erzielt.",
    "Brasilien ist mit fünf Titeln Rekord-Weltmeister.",
    "Oliver Kahn ist der einzige Torhüter, der als bester Spieler einer WM ausgezeichnet wurde (2002).",
    "Die schnellste Rote Karte der WM-Geschichte gab es nach 56 Sekunden.",
    "Pelé ist der jüngste Torschütze in einem WM-Finale (17 Jahre, 1958).",
    "Das erste offizielle Länderspiel fand 1872 zwischen Schottland und England statt.",
    "Der teuerste Transfer der Geschichte war Neymar für 222 Mio. € zu PSG.",
    "Der FC Bayern ist der einzige deutsche Klub, der das Triple zwei Mal gewonnen hat (2013 & 2020).",
    "Der Ball war 2010 bei Frank Lampards Lattenschuss klar hinter der Linie – Tor wurde nicht gegeben.",
    "Die meisten Tore in einem WM-Spiel erzielte Oleg Salenko (5 Tore für Russland 1994).",
    "Lionel Messi ist der Spieler mit den meisten Vorlagen in der WM-Geschichte.",
    "Die längste Serie ohne Niederlage im Profifußball: Italien (37 Spiele, 2018–2021).",
    "Maradona erzielte 1986 das berühmte 'Tor des Jahrhunderts' gegen England.",
    "Der erste Elfmeter in einem WM-Finale wurde 1974 von Paul Breitner verwandelt.",
    "Deutschland hat die meisten WM-Finalteilnahmen (8x).",
    "Das schnellste Tor in der WM-Geschichte fiel nach 11 Sekunden (Hakan Şükür, Türkei 2002)."
]

# Registrieren der Seite im Dash-Framework
dash.register_page(__name__, path="/", name="Startseite")

# Hauptlayout der Seite
layout = html.Div(
    style={
        "backgroundImage": "linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1430232324554-8f4aebd06683?q=80&w=3132&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "minHeight": "100vh",
        "padding": "3rem",
        "color": "white"
    },
    children=[
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("⚽ Fußball-Dashboard", className="display-4 animate__animated animate__fadeInDown", style={"color": "#ffffff"}),
                    html.P(
                        "Erkunde interaktive Statistiken und Analysen zu Transfers, Marktwerten, Positionen und mehr.",
                        className="lead animate__animated animate__fadeInUp",
                        style={"fontSize": "1.25rem", "color": "#dbe9f4"}
                    ),
                    html.Br(),
                    dcc.Link("🚀 Los geht’s", href="/geo_choropleth", className="btn btn-primary btn-lg animate__animated animate__fadeInRight")
                ], md=6),
            ], className="my-5"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("💡 Fußball-Fakt des Tages", className="card-title animate__animated animate__fadeInUp", style={"color": "white"}),
                            html.Div(id="fact-output", children=random.choice(facts), className="animate__animated animate__fadeInUp",
                                style={"fontSize": "1.1rem", "color": "white"},),
                            dbc.Button("🔄 Neuen Fakt anzeigen", id="fact-button", color="secondary",
                                       className="mt-3 animate__animated animate__fadeInUp")
                        ])
                    ], className="shadow-lg animate__animated animate__fadeInUp", style={
                        "backgroundColor": "rgba(255, 255, 255, 0.1)",  # halbtransparent
                        "backdropFilter": "blur(5px)",  # für leichten Unschärfeeffekt
                        "border": "1px solid rgba(255,255,255,0.2)"
                    })
                ], md=8)
            ], justify="center")
        ])
    ]
)

@callback(
    Output("fact-output", "children"),
    Input("fact-button", "n_clicks"),
    prevent_initial_call=True
)

# Callback-Funktion, um einen neuen Fakt anzuzeigen
def update_fact(n_clicks):
    return random.choice(facts)