
from pathlib import Path

import pandas as pd


NUMERIC_COLUMNS = [
    "popularity",
    "duration_ms",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "time_signature",
]


def clean_tracks(df):
    """Clean Spotify track data without deleting incomplete tracks."""
    cleaned = df.copy()

    # Standardize column names.
    cleaned.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in cleaned.columns
    ]

    # Remove unnecessary CSV index columns.
    index_columns = [
        column for column in cleaned.columns
        if column.startswith("unnamed:")
    ]
    cleaned = cleaned.drop(columns=index_columns)

    # Clean text values.
    text_columns = cleaned.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned[column] = (
            cleaned[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    # Convert numeric columns safely.
    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(
                cleaned[column], errors="coerce"
            )

    # Validate popularity values.
    if "popularity" in cleaned.columns:
        invalid = ~cleaned["popularity"].between(0, 100)
        cleaned.loc[invalid, "popularity"] = pd.NA

    # Validate track duration.
    if "duration_ms" in cleaned.columns:
        invalid = cleaned["duration_ms"] <= 0
        cleaned.loc[invalid, "duration_ms"] = pd.NA

    # Standardize explicit-content values.
    if "explicit" in cleaned.columns:
        values = cleaned["explicit"].astype("string").str.lower()
        cleaned["explicit"] = values.map({
            "true": True,
            "false": False,
            "1": True,
            "0": False,
        }).astype("boolean")

    # Remove exact duplicate rows only.
    cleaned = cleaned.drop_duplicates()

    return cleaned.reset_index(drop=True)


def load_tracks(path="data/spotify_tracks.csv"):
    """Load and clean the Spotify dataset."""
    csv_path = Path(path)

    if not csv_path.is_absolute():
        csv_path = Path(__file__).resolve().parent / csv_path

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Spotify dataset not found: {csv_path}"
        )

    df = pd.read_csv(csv_path)
    return clean_tracks(df)


def get_data_quality_report(df):
    """Summarize the dataset for cleaning verification."""
    return {
        "Total rows": len(df),
        "Total columns": len(df.columns),
        "Duplicate rows": int(df.duplicated().sum()),
        "Missing values": int(df.isna().sum().sum()),
        "Missing values by column": df.isna().sum().to_dict(),
    }
