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
    """Normalize column names, text, and known numeric fields."""
    cleaned = df.copy()
    cleaned.columns = [str(column).strip() for column in cleaned.columns]

    index_columns = [
        column
        for column in cleaned.columns
        if column.lower() == "unnamed: 0"
    ]
    cleaned = cleaned.drop(columns=index_columns)

    text_columns = cleaned.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)

    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    if "explicit" in cleaned.columns:
        explicit_values = cleaned["explicit"].astype("string").str.lower()
        cleaned["explicit"] = explicit_values.map(
            {"true": True, "false": False, "1": True, "0": False}
        ).astype("boolean")

    return cleaned.drop_duplicates().reset_index(drop=True)


def load_tracks(path="data/spotify_tracks.csv"):
    """Load the Spotify CSV relative to this project and clean it."""
    csv_path = Path(path)
    if not csv_path.is_absolute():
        csv_path = Path(__file__).resolve().parent / csv_path
    return clean_tracks(pd.read_csv(csv_path))