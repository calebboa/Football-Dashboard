# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, Input, Output, callback
import dash
import dash_bootstrap_components as dbc

# Registrieren der Seite im Dash-Framework
dash.register_page(__name__, path="/geo_choropleth", name="Länder-Vergleich")

# Hauptlayout der Seite
layout = html.Div([
    dbc.Container([
        html.Br(),
        html.H3("Talent und Kaufkraft im internationalen Fußball", style={'color': 'white'}),
        html.Br(),

        # Filteroptionen für die Karte
        dbc.Row([
            dbc.Col([
                html.Label("Darstellung", style={'color': 'white'}),
                # RadioItems für die Auswahl des Kartentyps
                dcc.RadioItems(
                    id='map-type',
                    options=[
                        {'label': 'Durchschn. Marktwert pro Nation', 'value': 'market_value'},
                        {'label': 'Transferausgaben pro Land', 'value': 'transfer_fee'}
                    ],
                    value='market_value',
                    labelStyle={'display': 'block', 'color': 'white'}
                )
            ], md=3),
            dbc.Col([
                html.Label("Top-N Länder", style={'color': 'white'}),
                # Slider für die Auswahl der Top-N Länder
                dcc.Slider(
                    id='top-n-slider',
                    min=10,
                    max=100,
                    step=10,
                    value=50,
                    marks={i: str(i) for i in range(10, 101, 10)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], md=6),
            dbc.Col([
                html.Label("Mindestwert", style={'color': 'white'}),
                # Input-Feld für den Mindestwert
                dcc.Input(
                    id='min-value-input',
                    type='number',
                    min=0,
                    step=500_000,
                    placeholder="Mindestwert in €",
                    style={'width': '100%'},
                    debounce=False
                )
            ], md=3)
        ]),

        html.Br(),
        dcc.Graph(id='geo-choropleth')
    ], fluid=True, style={'backgroundColor': 'black'})
])

@callback(
    Output('geo-choropleth', 'figure'),
    Input('map-type', 'value'),
    Input('top-n-slider', 'value'),
    Input('min-value-input', 'value')
)

def update_choropleth(map_type, top_n, min_value):
    # Überprüfen des Mindestwerts
    if not min_value:
        min_value = 0

    if map_type == 'market_value':
        # Daten einlesen
        df = pd.read_csv("fußball-dashboard/data/cleaned_transfersGit.csv")

         # Gruppieren der Daten nach Nationalität und Berechnung des Durchschnitts
        df = df[df['market_value'] >= min_value]
        agg = df.groupby('nationality', as_index=False)['market_value'].mean()
        agg['market_value'] /= 1_000_000
        agg = agg.nlargest(top_n, 'market_value')

        fig = go.Figure(go.Choropleth(
            locations=agg['nationality'],
            locationmode='country names',
            z=agg['market_value'],
            colorscale='viridis',
            colorbar_title='Durchschn. Marktwert in Mio. €'
        ))
        fig.update_layout(title_text='Durchschn. Marktwert pro Nationalität')

    else:
        # Daten einlesen
        df = pd.read_csv("fußball-dashboard/data/merged_transfers.csv")

        # Filterung der Daten nach Transfergebühren
        df = df[(df['transfer_fee'].notna()) & (df['transfer_fee'] >= min_value)]
        agg = df.groupby('team_ziel_country', as_index=False)['transfer_fee'].sum()
        agg['transfer_fee'] /= 1_000_000
        agg = agg.nlargest(top_n, 'transfer_fee')

        fig = go.Figure(go.Choropleth(
            locations=agg['team_ziel_country'],
            locationmode='country names',
            z=agg['transfer_fee'],
            colorscale='plasma',
            colorbar_title='Transferausgaben (€M)'
        ))
        fig.update_layout(title_text='Transferausgaben pro Land')

    fig.update_layout(
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='black',
        font=dict(color='white'),
        margin=dict(t=50, b=0, l=0, r=0)
    )
    return fig