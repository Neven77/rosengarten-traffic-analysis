from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


def extract_year_from_filename(file_path: Path) -> int | None:
    """Extract a 4-digit year (1900-2099) from a file name."""
    match = re.search(r"(19|20)\d{2}", file_path.stem)
    if not match:
        return None
    return int(match.group())


def read_csv_file(file_path: Path) -> pd.DataFrame:
    """Read a CSV file with automatic delimiter detection."""
    try:
        return pd.read_csv(file_path, sep=None, engine="python")
    except Exception as exc:
        raise ValueError(f"CSV konnte nicht gelesen werden: {file_path.name}. Fehler: {exc}") from exc


def ensure_year_column(df: pd.DataFrame, file_path: Path) -> pd.DataFrame:
    """Ensure the dataframe has a standardized 'year' column."""
    year_like_cols = [col for col in df.columns if str(col).strip().lower() == "year"]

    if len(year_like_cols) > 1:
        raise ValueError(
            f"Mehrere mögliche Year-Spalten in {file_path.name}: {year_like_cols}. "
            "Bitte CSV-Spalten bereinigen."
        )

    if len(year_like_cols) == 1:
        year_col = year_like_cols[0]
        if year_col != "year":
            df = df.rename(columns={year_col: "year"})
        return df

    extracted_year = extract_year_from_filename(file_path)
    if extracted_year is None:
        raise ValueError(
            f"Keine 'year'-Spalte und kein Jahr im Dateinamen gefunden: {file_path.name}. "
            "Erwartet wird z. B. 'traffic_2021.csv'."
        )

    df = df.copy()
    df["year"] = extracted_year
    return df


def validate_schema(current_columns: list[str], expected_columns: list[str], file_name: str) -> None:
    """Validate that all files share the same non-year columns."""
    current_set = set(current_columns)
    expected_set = set(expected_columns)

    if current_set != expected_set:
        missing = sorted(expected_set - current_set)
        extra = sorted(current_set - expected_set)
        raise ValueError(
            "Spalten stimmen nicht ueberein in "
            f"{file_name}. Fehlend: {missing if missing else '-'}, "
            f"zusaetzlich: {extra if extra else '-'}"
        )


def merge_traffic_data(raw_dir: Path, output_file: Path) -> None:
    csv_files = sorted(raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Keine CSV-Dateien gefunden in: {raw_dir}")

    merged_frames: list[pd.DataFrame] = []
    expected_non_year_columns: list[str] | None = None

    for csv_file in csv_files:
        df = read_csv_file(csv_file)
        df = ensure_year_column(df, csv_file)

        non_year_columns = [col for col in df.columns if col != "year"]

        if expected_non_year_columns is None:
            expected_non_year_columns = non_year_columns
        else:
            validate_schema(non_year_columns, expected_non_year_columns, csv_file.name)

        # Ensure a stable output order across all files.
        df = df[[*expected_non_year_columns, "year"]]
        merged_frames.append(df)

    combined_df = pd.concat(merged_frames, ignore_index=True)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(output_file, index=False)

    print(f"{len(csv_files)} Dateien zusammengefuehrt.")
    print(f"Ergebnis gespeichert unter: {output_file}")
    print(f"Anzahl Zeilen: {len(combined_df)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fuehrt alle Verkehrs-CSV-Dateien aus data/raw zusammen und speichert eine kombinierte Datei."
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw"),
        help="Ordner mit den Rohdaten-CSV-Dateien (Standard: data/raw)",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=Path("data/processed/traffic_data_combined.csv"),
        help="Pfad zur Ausgabe-CSV (Standard: data/processed/traffic_data_combined.csv)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    merge_traffic_data(raw_dir=args.raw_dir, output_file=args.output_file)


if __name__ == "__main__":
    main()
