# Import necessary libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
from plotly.subplots import make_subplots

url = "https://raw.githubusercontent.com/d2ski/football-transfers-data/refs/heads/main/dataset/transfers.csv"
df1 = pd.read_csv(url) # CSV file von URL ablesen

df2 = pd.read_csv("fußball-dashboard/data/players_transfers.csv",dtype={'age': str})

df2['age'] = pd.to_numeric(df2['age'], errors='coerce')  # Konvertiert 'age' zu numerisch, Fehler werden zu NaN
df2.dropna(subset=['age'], inplace=True)                 # Entfernt Zeilen, wo 'age' NaN ist
df2['age'] = df2['age'].astype(int)                      # Konvertiert 'age' zu int, nachdem NaN entfernt wurden

# Clean DataFrame 1
df1.rename(columns={
    "player_name": "name",
    "player_age": "age",
    "player_pos": "position",
    "player_nation": "nationality",
    "player_team": "team",
    "transfer_fee_amnt": "transfer_fee",
    "market_val_amnt":"market_value"}, inplace=True)

cols_drop1 = ['window','team_id','player_id','counter_team_id',  # Spalten, die entfernt werden sollen
              'counter_team_name','team_country','counter_team_country',
              'dir','transfer_id','is_free','is_loan','is_loan_end','is_retired',"transfer_id", "player_nation2"]

df1.drop(columns=cols_drop1, inplace=True, errors='ignore') # Entfernt die Spalten, die nicht mehr benötigt werden

df1['name'] = df1['name'].astype(str).str.strip().str.upper() # Konvertiert 'name' zu String, entfernt Leerzeichen und wandelt in Großbuchstaben um
df1['team_name']   = df1['team_name'].astype(str).str.strip().str.upper() 
df1['nationality'] = df1['nationality'].astype(str).str.upper() 
df1.dropna(subset=["age", "transfer_fee"], inplace=True) # Entfernt Zeilen, wo 'age' oder 'transfer_fee' NaN ist
df1 = df1[pd.to_numeric(df1["age"], errors="coerce").notna()] # Konvertiert 'age' zu numerisch, Fehler werden zu NaN und entfernt diese Zeilen
df1["age"] = df1["age"].astype(int) # Konvertiert 'age' zu int, nachdem NaN entfernt wurden
df1['league'] = df1['league'].replace('L1', 'GER1') # Ersetzt 'L1' durch 'GER1' in der 'league' Spalte

df1['transfer_fee'] = df1['transfer_fee'].astype(float).fillna(0) # Konvertiert 'transfer_fee' zu float und ersetzt NaN durch 0
df1['market_value'] = df1['market_value'].astype(float).fillna(0)

# Mapping/Umbennenung der Positionen
position_map = {
    'Centre-Forward': 'CF',
    'Left Winger': 'LW',
    'Right Winger': 'RW',
    'Attacking Midfield': 'AM',
    'Central Midfield': 'CM',
    'Defensive Midfield': 'DM',
    'Right Midfield': 'RM',
    'Left Midfield': 'LM',
    'Second Striker': 'ST',
    'Goalkeeper': 'GK',
    'Centre-Back': 'CB',
    'Left-Back': 'LB',
    'Right-Back': 'RB',
    "RB": "RB",
    "LB": "LB",
    "CB": "CB",
    "GK": "GK",
    "AM": "AM",
    "CM": "CM",
    "DM": "DM",
    "RM": "RM",
    "LM": "LM",
    "SS": "ST",
    "LW": "LW",
    "RW": "RW",
    "CF": "CF",

    # Fallbacks (wenn nötig):
    'Striker': 'ST',
    'Midfield': 'MF',
    'Forward': 'FW',
    'Defender': 'DF',
    "defence":"DF",
    "midfield": "MF",
    "attack":"ST"
}
df1['position'] = df1['position'].map(position_map).fillna(np.nan) # Füllt nicht gemappte Positionen mit NaN

# Spezialfälle manuell korrigieren
special_cases = {
   'england': 'United Kingdom',
    'wales': 'United Kingdom',
    'scotland': 'United Kingdom',
    'northern ireland': 'United Kingdom',
    'turkey': 'Turkey',
    'korea, south': 'South Korea',
    'korea, north': 'North Korea',
    'czechia': 'Czech Republic',
    'united states': 'United States of America',
    'russia': 'Russia',
    'réunion': 'Réunion',  # wird von Plotly als Teil Frankreichs behandelt, ggf. 'France'
    'bosnia-herzegovina': 'Bosnia and Herzegovina',
    'moldova, republic of': 'Moldova, Republic of',
    'venezuela, bolivarian republic of': 'Venezuela, Bolivarian Republic of',
    'syrian arab republic': 'Syrian Arab Republic',
    'palästina': 'Palestine',
    'palastina': 'Palestine',  
    'palestina': 'Palestine',  # alternative Schreibweise
    'guinea-bissau': 'Guinea-Bissau',
    'sao tome and principe': 'Sao Tome and Principe',
    'cape verde': 'Cabo Verde',
    'faroe islands': 'Faroe Islands',
    'new caledonia': 'New Caledonia',
    'curacao': 'Curaçao',
    'tahiti': 'French Polynesia',  
    'kosovo': 'Kosovo',  
    'the gambia': 'Gambia',
    'nan': None,
    'neukaledonien': 'New Caledonia',
    'hongkong': 'Hong Kong',
    'palästina': 'Palestine',
    'palästina': 'Palestine',
    'palästina': 'Palestine',
}

# Funktion zur Normalisierung der Ländernamen
# Diese Funktion verwendet die pycountry-Bibliothek, um Ländernamen zu normalisieren
def normalize_country(name):
    name_clean = str(name).strip().lower()

    if name_clean in special_cases:
        return special_cases[name_clean]
    
    try:
        return pycountry.countries.lookup(name).name
    except LookupError:
        return name.strip()  # Wenn kein Match, Originalname behalten

df1['nationality'] = df1['nationality'].apply(normalize_country) 
df1 = df1[df1['transfer_fee'] <= 200_000_000] # Filtert Transfers über 200 Mio. Euro aus

# Schritt 1: Filtern auf höchsten Marktwert pro Spieler+Saison
max_market_df = df1[df1.groupby(['name', 'season'])['market_value'].transform('max') == df1['market_value']]

# Schritt 2: Doppelte Zeilen (z. B. Mo Salah 4x) auf eine reduzieren
df1 = max_market_df.drop_duplicates(subset=['name'], keep='first').reset_index(drop=True)

# Spieler pro Saison zählen, bei wie vielen Vereinen sie spielen
player_season_club_counts = df1.groupby(['name'])['team_name'].nunique()

# Funktion zur Klassifizierung der Transfers
def classify_transfer_direction(row):
    key = (row['season'], row['name'])
    club_count = player_season_club_counts.get(key, 1)
    
    if club_count > 1:
        # Spieler bei mehreren Vereinen innerhalb einer Saison
        if row['transfer_fee'] > 0:
            return 'in'
        else:
            return 'out'
    else:
        # Spieler nur bei einem Verein in dieser Saison
        if row['transfer_fee'] > 0:
            return 'in'
        elif row['transfer_fee'] == 0 and row['market_value'] > 0:
            return 'out'
        else:
            return 'unknown'

# Anwenden und neue Spalte erstellen
df1['transfer_direction'] = df1.apply(classify_transfer_direction, axis=1)
df1 = df1[df1['transfer_direction'] == 'in']

# Dataframe 1 als CSV speichern
df1.to_csv("fußball-dashboard/data/cleaned_transfersGit.csv", index=False) 

# Clean up the DataFrame 2
df2.rename(columns={
    "team_B_name":"team_ziel_name",
    "team_A_name": "team_herkunft_name",
    "player_pos": "position",
    "player_name": "name",
    "team_A_league": "leagueHerkunft",
    "team_B_league": "leagueZiel",
    "role": "position",
    "team_A_country": "team_herkunft_country",
    "team_B_country": "team_ziel_country",
    }, inplace=True)


# Spalten, die entfernt werden sollen
cols_drop2 = ['team_A_tfm_name', 'team_A_id', 'team_B_tfm_name', 'player_id', 'team_A_league_tfm',
              'player_tfm_name', "team_B_id", "loan_status", "team_B_league_tfm", "value", "cost"]
df2.drop(columns=cols_drop2, inplace=True, errors='ignore')

df2['name'] = df2['name'].astype(str).str.strip().str.upper() # Konvertiert 'name' zu String, entfernt Leerzeichen und wandelt in Großbuchstaben um
df2['team_ziel_name'] = df2['team_ziel_name'].astype(str).str.strip().str.upper()
df2['team_herkunft_name'] = df2['team_herkunft_name'].astype(str).str.strip().str.upper()
df2['leagueZiel'] = df2['leagueZiel'].astype(str).str.strip().str.upper()
df2['leagueHerkunft'] = df2['leagueHerkunft'].astype(str).str.strip().str.upper()
df2['nationality'] = df2['nationality'].astype(str).str.strip().str.upper()
df2["team_ziel_country"] = df2["team_ziel_country"].astype(str).str.strip().str.upper()
df2["team_herkunft_country"] = df2["team_herkunft_country"].astype(str).str.strip().str.upper()
df2['season'] = df2['season'].str.slice(stop=4).astype(int)
df2.dropna(subset=['name','season'], inplace=True) # Entfernt Zeilen, wo 'name' oder 'season' NaN ist

df2.drop_duplicates(subset=['name', 'season'], keep='first', inplace=True) # Entfernt Duplikate basierend auf 'name' und 'season'

df2['position'] = df2['position'].map(position_map).fillna(np.nan) # Füllt nicht gemappte Positionen mit NaN
df2['position']=df2['position'].replace('SS', 'ST')
df2['nationality'] = df2['nationality'].apply(normalize_country)

# DataFrame 2 als CSV speichern
df2.to_csv("fußball-dashboard/data/cleaned_players_transfers.csv", index=False)

# Merge the two DataFrames on 'name' and 'season'
merged_df = pd.merge(df1, df2, on=['name', 'season'], how='inner')

merged_df.rename(columns={
    'age_x': 'age',
    'nationality_x': 'nationality',
    'position_x': 'position',
}, inplace=True)

merged_df['team_ziel_country'] = merged_df['team_ziel_country'].apply(normalize_country) # Normalisiert die Ländernamen im 'team_ziel_country'

merged_df.drop(columns=['age_y', 'nationality_y', 'position_y'], inplace=True, errors='ignore')

# Save the merged DataFrame to a CSV file
merged_df.to_csv("fußball-dashboard/data/merged_transfers.csv", index=False)

# # print(df1['nationality'].unique())
# print("Anzahl UK-Spieler:", len(df1[df1['nationality'] == 'United Kingdom']))
# print(df1[df1['nationality'] == 'United Kingdom']['market_value'].describe())

# print("Anzahl Canada-Spieler:", len(df1[df1['nationality'] == 'Canada']))
# print(df1[df1['nationality'] == 'Canada']['market_value'].describe())


