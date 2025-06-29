# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/transfer_spending", name="Transferausgaben")

# Daten einlesen
df = pd.read_csv("fußball-dashboard/data/merged_transfers.csv")

# Mindesttransfergebühr von 5 Mio. €
filtered_df = df[df['transfer_fee'] >= 5_000_000] 

# Filterwerte vorbereiten
clubs_available = sorted(filtered_df['team_name'].dropna().unique())
seasons_available = sorted(filtered_df['season'].dropna().unique())
leagues_available = sorted(filtered_df['league'].dropna().unique())

# Hauptlayout der Seite
layout = html.Div([ 
    # Container für die gesamte Seite
    dbc.Container([
        html.Br(),
        html.H3("Transferausgaben pro Verein nach Saison", style={'color': 'white'}),
        html.Br(),

        # Filteroptionen für Saisons, Ligen und Clubs
        dbc.Row([
            dbc.Col([
                html.Label("Saisons", style={'color': 'white'}),
                dcc.Dropdown(
                    id='transfer-season-filter',
                    options=[{'label': str(s), 'value': s} for s in seasons_available],
                    value=seasons_available[-10:],
                    multi=True
                )
            ], md=3),
            dbc.Col([
                html.Label("Ligen", style={'color': 'white'}),
                dcc.Dropdown(
                    id='league-filter',
                    options=[{'label': l, 'value': l} for l in leagues_available],
                    multi=True
                )
            ], md=3),
            dbc.Col([
                html.Label("Clubs", style={'color': 'white'}),
                dcc.Dropdown(
                    id='club-filter',
                    options=[{'label': c, 'value': c} for c in clubs_available],
                    multi=True
                )
            ], md=3),
        ]),
        html.Br(),
        dcc.Graph(id='transfer-trend-graph')
    ], fluid=True, style={'backgroundColor': 'black'})
])

@callback(
    Output('transfer-trend-graph', 'figure'),
    Input('transfer-season-filter', 'value'),
    Input('league-filter', 'value'),
    Input('club-filter', 'value')
)

def update_transfer_trend(seasons, leagues, clubs):
    dff = df.copy()
    # Mindestgebühr von 5 Mio. € anwenden
    dff = dff[dff['transfer_fee'] >= 5_000_000]
    if seasons:
        dff = dff[dff['season'].isin(seasons)] 
    if leagues:
        dff = dff[dff['league'].isin(leagues)]
    if clubs:
        dff = dff[dff['team_name'].isin(clubs)]

    agg = dff.groupby(['team_name', 'season'])['transfer_fee'].sum().reset_index()
    agg['transfer_fee'] = agg['transfer_fee'] / 1_000_000

    # Top-N Clubs bei zu vielen Mannschaften automatisch filtern 
    top_clubs = agg.groupby('team_name')['transfer_fee'].sum().nlargest(10).index
    agg = agg[agg['team_name'].isin(top_clubs)]

    fig = px.line(
        agg,
        x='season',
        y='transfer_fee',
        color='team_name',
        markers=True,
        labels={'transfer_fee': 'Ausgaben (€M)', 'season': 'Saison', 'team_name': 'Verein'},
        title='Transferausgaben pro Saison'
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(dtick=1, color='white', title='Saison', tickfont=dict(color='white')),
        yaxis=dict(title='Ausgaben (€M)', color='white', tickfont=dict(color='white')),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white'),
        legend=dict(font=dict(color='white'))
    )
    return fig