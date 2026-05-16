# Changelog

## 2026-05-16
- Power-BI-Dashboard abgeschlossen (`powerbi/zurich_traffic_dashboard.pbix`).
- Zwei Dashboard-Screenshots hinzugefügt (`img/Executive-Overview.png`, `img/Interactive-Analysis.png`).
- README ergänzt: Beschreibung der Seiten "Executive Overview" und "Interactive Traffic Analysis" inkl. Bilder.
- README-Kurzbeschreibung präzisiert: Open Data -> Python-Zusammenführung -> Jupyter-Analyse -> Power-BI-Dashboard.

## 2026-05-14
- Projektstruktur für Datenpipeline und Power BI angelegt (`data`, `scripts`, `notebooks`, `powerbi`).
- Robustes Merge-Skript `scripts/merge_traffic_data.py` erstellt.
- `requirements.txt` mit Pandas hinzugefügt.
- Professionelles `README.md` mit Workflow, Struktur und Erweiterungen erstellt.
- `.gitignore` für Python, Jupyter, Power BI und lokale Dateien vorbereitet.
- Notebook-Startdatei `notebooks/traffic_analysis.ipynb` angelegt.
- Bestehende PBIX-Datei nach `powerbi/` kopiert (Originaldatei im Root ggf. gesperrt/offen).
- `scripts/merge_traffic_data.py` überarbeitet und klar strukturiert.
- CSV-Einlesen im Skript beschleunigt (Delimiter-Erkennung, C-Engine) und Fortschrittsanzeige ergänzt.
- Konkrete Open-Data-Zürich-Quelle im README ergänzt (inkl. Abrufdatum).
- Notebook um eine einfache Analyse erweitert (Zeilen/Spalten, Datentypen, Jahre, Top-Klassen, Missing Values).
- Im Notebook eine minimale Transformation für Power BI ergänzt: `Datum` ohne Zeit/Zeitzone als `YYYY-MM-DD`, Export nach `data/processed/traffic_data_powerbi.csv`.
- Notebook-Transformation angepasst: Uhrzeit bleibt erhalten, nur Zeitzone wird entfernt (`YYYY-MM-DD HH:MM:SS`) für bessere Traffic-Spitzenanalyse in Power BI.
- Notebook-Export für Power BI: nicht benötigte Spalten `year` und `Intervall` entfernt.
- Notebook-Export: `Status` entfernt, da für das Dashboard nicht benötigt.
- Notebook-Export: `Standort` entfernt (nur ein Wert im Datensatz).
