# Zurich Open Data Traffic Analysis

## Kurzbeschreibung
Ein schlankes Portfolio-Projekt, das zeigt, wie mehrere Rohdaten-CSV-Dateien aus einer öffentlichen Datenquelle strukturiert, bereinigt und zu einer einheitlichen Analysebasis zusammengeführt werden.

## Ziel des Projekts
Das Projekt erstellt aus mehreren Jahres-CSV-Dateien eine bereinigte Gesamttabelle (`traffic_data_combined.csv`).
Diese Datei dient als Datenbasis für ein Power-BI-Dashboard (`.pbix`).

## Datenquelle
Open Data Zürich (Link wird später ergänzt).

## Projektstruktur

```text
rosengarten-traffic-analysis/
|
|-- data/
|   |-- raw/
|   |-- processed/
|
|-- scripts/
|   |-- merge_traffic_data.py
|
|-- notebooks/
|   |-- traffic_analysis.ipynb
|
|-- powerbi/
|   |-- zurich_traffic_dashboard.pbix
|
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- LICENSE
|-- CHANGELOG.md
```

## Workflow
1. Rohdaten als CSV in `data/raw/` ablegen.
2. Python/Pandas-Skript ausfuehren.
3. Kombinierte Datei in `data/processed/traffic_data_combined.csv` erzeugen.
4. Datei in Power BI laden und Dashboard aktualisieren.

```text
Raw Data -> Python/Pandas Transformation -> Processed CSV -> Power BI Dashboard
```

## Verwendete Technologien
- Python
- Pandas
- Power BI
- GitHub

## Python-Skript: `scripts/merge_traffic_data.py`
Das Skript:
- liest alle CSV-Dateien aus `data/raw/` ein,
- ergänzt bei Bedarf die Spalte `year` aus dem Dateinamen,
- prüft, ob die Spaltenstruktur zwischen den Dateien zusammenpasst,
- führt alle Dateien in eine Tabelle zusammen,
- speichert das Ergebnis als `data/processed/traffic_data_combined.csv`.

### Ausführung

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/merge_traffic_data.py
```

Optional mit benutzerdefinierten Pfaden:

```bash
python scripts/merge_traffic_data.py --raw-dir data/raw --output-file data/processed/traffic_data_combined.csv
```

## Power-BI-Dashboard
Die Datei `powerbi/zurich_traffic_dashboard.pbix` ist die Dashboard-Datei für Visualisierungen und KPI-Auswertungen auf Basis der kombinierten CSV.
Es wird bewusst mit einer einzelnen `.pbix` gearbeitet (kein Power BI Project Structure).

## Charakter des Projekts
Dies ist ein einfaches Portfolio-Prototyp-Projekt.
Der Fokus liegt auf Nachvollziehbarkeit, klarer Datenpipeline und reproduzierbarem Workflow statt auf maximaler Komplexität.

## Sinnvolle Erweiterungen
- Weitere Jahre in die Zeitreihe aufnehmen
- Zusätzliche KPIs (z. B. Peak-Stunden, Wochentagsmuster)
- Kombination mit Einwohnerdaten
- Kombination mit Parkplatzdaten
- Regionale Vergleiche innerhalb Zürichs

## Struktur-Check und empfohlene Verbesserungen
Die gewünschte Struktur ist für ein Portfolio-Projekt sehr gut geeignet.
Optional (später) sinnvoll:
- `data/raw/.gitkeep` und `data/processed/.gitkeep` für leere Ordner im Repo
- `tests/` für einfache Datenqualitäts-Checks
- `docs/` für Screenshots des Dashboards
