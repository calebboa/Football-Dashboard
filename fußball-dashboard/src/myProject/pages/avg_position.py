# Import necessary libraries
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/avg_position", name="Ablösesummen nach Position")

df = pd.read_csv("fußball-dashboard/data/merged_transfers.csv") # Daten einlesen
positions_available = sorted(df['position'].dropna().unique()) # Verfügbare Positionen
seasons_available = sorted(df['season'].dropna().unique()) # Verfügbare Saisons

layout = html.Div([
    dbc.Container([
        html.Br(),
        html.H3("Durchschnittliche Ablösesummen je Position", style={'color': 'white'}), 
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Label("Saisons", style={'color': 'white'}),
                # RangeSlider für Saisons
                dcc.RangeSlider(
                    id='avg-seasons',
                    min=min(seasons_available),
                    max=max(seasons_available),
                    value=[max(seasons_available) - 7, max(seasons_available)],
                    marks={int(s): str(s) for s in seasons_available},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], md=10),
            dbc.Col([
                html.Label("Positionen", style={'color': 'white'}),
                dcc.Dropdown(
                    id='avg-positions',
                    options=[{'label': p, 'value': p} for p in positions_available],
                    multi=True
                )
            ], md=5)
        ]),
        html.Br(),
        dcc.Graph(id="avg-fee-bar")
    ], fluid=True, style={'backgroundColor': 'black'})
])

@callback( # Callback (Reaktionen auf Nutzereingaben) für die Aktualisierung des Balkendiagramms
    Output("avg-fee-bar", "figure"), # Ausgabe des Diagramms
    Input("avg-seasons", "value"), # Eingabe für den Saisonbereich
    Input("avg-positions", "value") # Eingabe für die ausgewählten Positionen
)

def update_bar_chart(season_range, positions):
    dff = df.copy()
    dff = dff[dff['transfer_fee'] >= 1_000_000] # Filter für Ablösesummen >= 1 Mio. €

    start_year, end_year = season_range # definieren des Bereichs
    dff = dff[(dff['season'] >= start_year) & (dff['season'] <= end_year)] 
    if positions:
        dff = dff[dff['position'].isin(positions)] # Filter für ausgewählte Positionen

    agg = dff.groupby('position')['transfer_fee'].mean().reset_index() # Durchschnittliche Ablösesumme pro Position
    agg['avg_transfer_fee'] = agg['transfer_fee'] / 1_000_000 # Umwandlung in Millionen €
    agg = agg.sort_values('avg_transfer_fee', ascending=False) # Sortierung nach durchschnittlicher Ablösesumme

    colors = plotly.colors.qualitative.Plotly

    bar_colors = [colors[i % len(colors)] for i in range(len(agg))]

    fig = go.Figure(data=go.Bar(
        x=agg['position'], # Positionen auf der x-Achse
        y=agg['avg_transfer_fee'], # Durchschnittliche Ablösesummen auf der y-Achse
        text=[f"{v:.2f}" for v in agg['avg_transfer_fee']], # Textbeschriftung der Balken
        textposition='auto', # Automatische Positionierung der Textbeschriftung
        marker_color=bar_colors 
    ))

    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white'),
        xaxis=dict(title='Position', tickfont=dict(color='white')),
        yaxis=dict(title='Durchschn. Ablösesumme in Mio €', tickfont=dict(color='white'))
    )
    return fig