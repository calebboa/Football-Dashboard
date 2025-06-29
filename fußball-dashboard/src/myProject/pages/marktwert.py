# Import necessary libraries
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/marktwert", name="Marktwertentwicklung")

# Daten einlesen
df = pd.read_csv("fußball-dashboard/data/merged_transfers.csv")
positions_available = sorted(df['position'].dropna().unique())
seasons_available = sorted(df['season'].dropna().unique())

# Hauptlayout der Seite
layout = html.Div([
    # Container für die gesamte Seite
    dbc.Container([
        html.Br(),
        html.H3("Marktwertentwicklung: Junge vs. ältere Spieler", style={'color': 'white'}),
        html.Br(),

        # Filteroptionen für Positionen, Saisons und Altersgrenze
        dbc.Row([
            dbc.Col([
                html.Label("Position", style={'color': 'white'}),
                # Dropdown für Positionen
                dcc.Dropdown(
                    id='position-filter',
                    options=[{'label': pos, 'value': pos} for pos in positions_available],
                    multi=True,
                    placeholder="Wähle Position(en)"
                )
            ], md=4),
            dbc.Col([
                html.Label("Saisons", style={'color': 'white'}),
                # RangeSlider für Saisons
                dcc.RangeSlider(
                    id='season-range-slider',
                    min=min(seasons_available),
                    max=max(seasons_available),
                    value=[min(seasons_available), max(seasons_available)],  # Default: ganze Range
                    marks={int(season): str(season) for season in seasons_available},
                    tooltip={"placement": "bottom", "always_visible": True},
                    step=1
                )
            ], md=4),

            dbc.Col([
                html.Label("Altersgrenze (jung vs. alt)", style={'color': 'white'}),
                # Slider für Altersgrenze
                dcc.Slider(
                    id='age-cutoff-slider',
                    min=18,
                    max=35,
                    step=1,
                    value=23,
                    marks={i: str(i) for i in range(18, 36, 2)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], md=4)
        ]),

        html.Br(),
        dcc.Graph(id='market-trend-graph')
    ], fluid=True, style={'backgroundColor': 'black'})
])

@callback(
    Output('market-trend-graph', 'figure'),
    Input('position-filter', 'value'),
    Input('season-range-slider', 'value'),
    Input('age-cutoff-slider', 'value')
)

def update_market_trend(positions, season_range, cutoff_age):
    dff = df.copy()
    # Mindestwert von 0 für Marktwert
    dff = dff[dff['market_value'] >= 0]
    if positions:
        dff = dff[dff['position'].isin(positions)]
    if season_range and len(season_range) == 2:
        dff = dff[(dff['season'] >= season_range[0]) & (dff['season'] <= season_range[1])]

    dff['age_group'] = np.where(dff['age'] < cutoff_age, 'jung', 'alt')
    grouped = dff.groupby(['season', 'age_group'])['market_value'].mean().reset_index()
    grouped['market_value'] = grouped['market_value'] / 1_000_000

    fig = go.Figure()
    colors = {
    'jung': 'red',
    'alt': 'green'
    }

    # Daten für die Altersgruppen hinzufügen
    for age_group in grouped['age_group'].unique():
        data = grouped[grouped['age_group'] == age_group]
        fig.add_trace(go.Scatter(
            x=data['season'],
            y=data['market_value'],
            mode='markers',
            name=f'Altersgruppe: {age_group}',
             marker=dict(
            size=10,
            color=colors.get(age_group, 'gray')  # falls mal was fehlt
        )
        ))

    fig.update_layout(
        title='Ø Marktwert nach Saison (Mio €)',
        xaxis=dict(title='Saison', tickmode='linear', dtick=1, color='white', tickfont=dict(color='white')),
        yaxis=dict(title='Ø Marktwert (in Mio €)', color='white', tickfont=dict(color='white')),
        paper_bgcolor='black',
        plot_bgcolor='black',
        hovermode='x unified',
        legend=dict(font=dict(color='white')),
        font=dict(color='white')
    )
    return fig