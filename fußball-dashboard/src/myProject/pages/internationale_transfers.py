# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/internationale_transfers", name="Internationale Transfers")

# Daten laden
df = pd.read_csv("fußball-dashboard/data/cleaned_players_transfers.csv")

# Top 5 Länder
top5 = ['ENGLAND', 'GERMANY', 'SPAIN', 'FRANCE', 'ITALY']

# Initialfilterung
df = df[
    (df['team_herkunft_country'].isin(top5)) &
    (df['team_ziel_country'].isin(top5)) &
    (df['team_herkunft_country'] != df['team_ziel_country'])
].copy()

# Auswahloptionen
countries_available = sorted(set(df['team_herkunft_country']).union(df['team_ziel_country']))

# Hauptlayout der Seite
layout = html.Div([
    # Container für die gesamte Seite
    dbc.Container([
        html.Br(),
        html.H3("Internationale Transferströme (Top-5-Länder)", style={'color': 'white'}),
        html.Br(),

        dbc.Row([
            dbc.Col([
                html.Label("Filter: Herkunftsländer", style={'color': 'white'}),
                # Dropdown für Herkunftsländer
                dcc.Dropdown(
                    id='sankey-source-filter',
                    options=[{'label': c, 'value': c} for c in countries_available],
                    multi=True,
                    placeholder="Alle"
                )
            ], md=6),
            dbc.Col([
                html.Label("Filter: Zielländer", style={'color': 'white'}),
                # Dropdown für Zielländer
                dcc.Dropdown(
                    id='sankey-target-filter',
                    options=[{'label': c, 'value': c} for c in countries_available],
                    multi=True,
                    placeholder="Alle"
                )
            ], md=6),
        ]),
        html.Br(),
        dcc.Graph(id='sankey-graph')
    ], fluid=True, style={'backgroundColor': 'black'})
])

@callback(
    Output('sankey-graph', 'figure'),
    Input('sankey-source-filter', 'value'),
    Input('sankey-target-filter', 'value')
)
def update_sankey(source_filter, target_filter):
    dff = df.copy()

    if source_filter:
        dff = dff[dff['team_herkunft_country'].isin(source_filter)]
    if target_filter:
        dff = dff[dff['team_ziel_country'].isin(target_filter)]

    # Aggregation
    agg = dff.groupby(['team_herkunft_country', 'team_ziel_country']).size().reset_index(name='count')
    all_countries = pd.unique(agg[['team_herkunft_country', 'team_ziel_country']].values.ravel())
    label_to_index = {country: idx for idx, country in enumerate(all_countries)}

    agg['source_idx'] = agg['team_herkunft_country'].map(label_to_index)
    agg['target_idx'] = agg['team_ziel_country'].map(label_to_index)

    # Farbzuordnung je Herkunftsland
    color_map = {
        'FRANCE': 'rgb(0, 85, 124)',
        'GERMANY': 'rgb(255, 204, 0)',
        'SPAIN': 'rgb(170, 21, 27)',
        'ITALY': 'rgb(0, 140, 69)',
        'ENGLAND': 'rgb(255, 242, 249)'
    }
    agg['color'] = agg['team_herkunft_country'].map(color_map)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=list(all_countries),
            color='rgba(200,200,200,0.9)'
        ),
        link=dict(
            source=agg['source_idx'],
            target=agg['target_idx'],
            value=agg['count'],
            color=agg['color']         )
    )])

    fig.update_layout(
        title='Häufigkeit der Transfers zwischen Ländern',
        font=dict(size=12, color='white'),
        paper_bgcolor='black',
        plot_bgcolor='black'
    )

    return fig