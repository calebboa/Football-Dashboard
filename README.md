# ⚽ Fußball-Transfer-Dashboard
<img width="1462" alt="Bildschirmfoto 2025-06-29 um 19 30 03" src="https://github.com/user-attachments/assets/22bd90aa-1132-4fc8-80f3-0e659d50e778" />

Ein interaktives Dashboard zur Analyse von Fußball-Transfers, Marktwerten und internationalen Transferströmen.

## 📂 Projektstruktur

```bash
fussball-dashboard/
├── data/                   # Rohdaten und bereinigte Datensätze
│   ├── players_transfers.csv
│   ├── cleaned_players_transfers.csv
│   ├── cleaned_transfersGit.csv
│   └──  merged_transfers.csv
├── app.py                  # Hauptanwendung
├── datasets.py             # Datenbereinigung und -verarbeitung
├── pages/
│   ├── home.py             # Startseite
│   ├── marktwert.py        # Marktwertanalyse
│   ├── transfer_spending.py # Transferausgaben
│   ├── avg_position.py     # Positionen-Analyse
│   ├── geo_choropleth.py   # Ländervergleich
│   └── internationale_transfers.py # Transferströme
└── README.md               # Diese Datei
```

## 📌 Features

- **Marktwertanalyse**: Vergleich der Marktwerte junger vs. älterer Spieler nach Position
  <img width="1462" alt="Bildschirmfoto 2025-06-29 um 19 31 56" src="https://github.com/user-attachments/assets/3bfd3f45-00fa-4b9a-aa0f-69046fecb141" />

- **Transferausgaben**: Visualisierung der Transferausgaben von Vereinen und Ligen
  <img width="1462" alt="Bildschirmfoto 2025-06-29 um 19 32 59" src="https://github.com/user-attachments/assets/fe8b12ea-6823-46ca-a26a-dc034bd057cb" />

- **Positionen**: Durchschnittliche Ablösesummen nach Spielerpositionen
  <img width="1462" alt="Bildschirmfoto 2025-06-29 um 19 33 37" src="https://github.com/user-attachments/assets/6f17b434-9ada-4a38-ba96-80a8bf2ae30f" />

- **Ländervergleich**: Choropleth-Karten für Marktwerte und Transferausgaben nach Nationen
  <img width="1462" alt="Bildschirmfoto 2025-06-30 um 10 03 52" src="https://github.com/user-attachments/assets/b2a1f650-382b-4726-ab43-70bd4b783292" />
  <img width="1462" alt="Bildschirmfoto 2025-06-30 um 10 04 17" src="https://github.com/user-attachments/assets/c23de5be-319d-49f6-b902-f07dc1111a2b" />


- **Internationale Transfers**: Sankey-Diagramm für Transferströme zwischen Top-Ligen
  <img width="1462" alt="Bildschirmfoto 2025-06-29 um 19 35 39" src="https://github.com/user-attachments/assets/ea2fe674-3abc-4e70-a4c9-d17503be5993" />


## 🛠 Technologien

- Python 3
- Dash/Plotly für interaktive Visualisierungen
- Pandas für Datenverarbeitung
- Bootstrap für das responsive Design
- GitHub Pages für die Bereitstellung (optional)

## 📊 Datenquellen

- Transferdaten von [Football Transfers GitHub](https://github.com/d2ski/football-transfers-data)
- Transferdaten aus Mendeley Data https://data.mendeley.com/datasets/rv7hktj86h/1?.com

## 🚀 Installation

1. Repository klonen:
   ```bash
   git clone https://github.com/dein-username/Football-Dashboard.git
   cd fussball-dashboard

2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

4. Dashboard starten:
   ```bash
   python app.py

## 🎨 Seitenübersicht

1. Startseite: Willkommensseite mit random Fußball-Fakten
2. Marktwertentwicklung: Vergleich junger vs. älterer Spieler
3. Transferausgaben: Analyse der Ausgaben pro Verein
4. Ablösesummen: Durchschnittliche Transfergebühren nach Position
5. Länder-Vergleich: Geografische Darstellung von Marktwerten und Ausgaben
6. Internationale Transfers: Visualisierung von Transferströmen zwischen Ligen
