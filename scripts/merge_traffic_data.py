import re
from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("data/processed/traffic_data_combined.csv")


def extract_year_from_filename(file_path: Path) -> int | None:
    """Extract a year like 2024 from the file name."""
    match = re.search(r"(19|20)\d{2}", file_path.stem)
    if not match:
        return None
    return int(match.group())


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize header quirks (BOM, spaces, extra quotes) across files."""
    cleaned_columns = []
    for col in df.columns:
        cleaned = str(col).replace("\ufeff", "").strip().strip('"').strip("'")
        cleaned_columns.append(cleaned)
    df.columns = cleaned_columns
    return df


def detect_delimiter(file_path: Path) -> str:
    """Detect a likely delimiter from the header/first lines."""
    sample = file_path.read_text(encoding="utf-8-sig", errors="ignore")[:10000]
    lines = [line for line in sample.splitlines() if line.strip()][:5]
    if not lines:
        raise ValueError(f"Datei ist leer oder unlesbar: {file_path.name}")

    candidates = [";", ",", "\t", "|"]
    counts = {sep: sum(line.count(sep) for line in lines) for sep in candidates}
    best_sep = max(counts, key=counts.get)

    if counts[best_sep] == 0:
        raise ValueError(
            f"Kein Trennzeichen erkannt in {file_path.name}. Erwartet: ; , TAB oder |"
        )
    return best_sep


def main() -> None:
    csv_files = sorted(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Keine CSV-Dateien gefunden in: {RAW_DIR}")

    dataframes = []
    expected_columns: list[str] | None = None

    for index, csv_file in enumerate(csv_files, start=1):
        print(f"[{index}/{len(csv_files)}] Lese Datei: {csv_file.name}")
        try:
            delimiter = detect_delimiter(csv_file)
            df = pd.read_csv(
                csv_file,
                sep=delimiter,
                encoding="utf-8-sig",
                engine="c",
                low_memory=False,
            )
        except Exception as exc:
            raise ValueError(f"CSV konnte nicht gelesen werden: {csv_file.name}. Fehler: {exc}") from exc

        df = normalize_column_names(df)

        # Falls keine year-Spalte vorhanden ist, Jahr aus Dateiname verwenden.
        if "year" not in df.columns:
            year = extract_year_from_filename(csv_file)
            if year is None:
                raise ValueError(
                    f"Keine 'year'-Spalte und kein Jahr im Dateinamen gefunden: {csv_file.name}"
                )
            df["year"] = year

        current_columns = list(df.columns)
        if expected_columns is None:
            expected_columns = current_columns
        elif set(current_columns) != set(expected_columns):
            missing = sorted(set(expected_columns) - set(current_columns))
            extra = sorted(set(current_columns) - set(expected_columns))
            raise ValueError(
                "Spalten stimmen nicht ueberein in "
                f"{csv_file.name}. Fehlend: {missing if missing else '-'}, "
                f"zusaetzlich: {extra if extra else '-'}"
            )

        # Einheitliche Spaltenreihenfolge wie in der ersten Datei.
        df = df[expected_columns]
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(OUTPUT_FILE, index=False)

    print(f"{len(csv_files)} Dateien zusammengefuehrt.")
    print(f"Ergebnis gespeichert unter: {OUTPUT_FILE}")
    print(f"Anzahl Zeilen: {len(combined_df)}")


if __name__ == "__main__":
    main()
