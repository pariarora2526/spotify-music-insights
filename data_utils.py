from pathlib import Path

import numpy as np
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

AUDIO_FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
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
        column
        for column in cleaned.columns
        if column.startswith("unnamed:")
    ]
    cleaned = cleaned.drop(columns=index_columns)

    # Remove leading/trailing whitespace from text.
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
            cleaned[column] = cleaned[column].replace(
                [np.inf, -np.inf], np.nan
            )

    # Popularity must be between 0 and 100.
    if "popularity" in cleaned.columns:
        invalid = ~cleaned["popularity"].between(0, 100)
        cleaned.loc[invalid, "popularity"] = np.nan

    # Audio features must be between 0 and 1.
    for column in AUDIO_FEATURE_COLUMNS:
        if column in cleaned.columns:
            invalid = ~cleaned[column].between(0, 1)
            cleaned.loc[invalid, column] = np.nan

    # Spotify track duration must be positive.
    if "duration_ms" in cleaned.columns:
        invalid = cleaned["duration_ms"] <= 0
        cleaned.loc[invalid, "duration_ms"] = np.nan

    # Tempo must be positive.
    if "tempo" in cleaned.columns:
        invalid = cleaned["tempo"] <= 0
        cleaned.loc[invalid, "tempo"] = np.nan

    # Key values should be between 0 and 11.
    if "key" in cleaned.columns:
        invalid = ~cleaned["key"].between(0, 11)
        cleaned.loc[invalid, "key"] = np.nan

    # Mode is binary: 0 or 1.
    if "mode" in cleaned.columns:
        invalid = ~cleaned["mode"].isin([0, 1])
        cleaned.loc[invalid, "mode"] = np.nan

    # Standardize explicit-content values.
    if "explicit" in cleaned.columns:
        values = cleaned["explicit"].astype("string").str.lower()

        cleaned["explicit"] = values.map({
            "true": True,
            "false": False,
            "1": True,
            "0": False,
        }).astype("boolean")

    # Remove exact duplicate records only.
    cleaned = cleaned.drop_duplicates()

    return cleaned.reset_index(drop=True)


def load_tracks(path="data/spotify_tracks.csv"):
    """Load the CSV and return cleaned data."""
    csv_path = Path(path)

    if not csv_path.is_absolute():
        csv_path = Path(__file__).resolve().parent / csv_path

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Spotify dataset not found: {csv_path}"
        )

    df = pd.read_csv(csv_path, low_memory=False)

    return clean_tracks(df)


def get_data_quality_report(df):
    """Return a summary of missing values and duplicate records."""
    missing = df.isna().sum()

    if len(df) > 0:
        missing_percent = (missing / len(df) * 100).round(2)
    else:
        missing_percent = missing.astype(float)

    return {
        "Total rows": len(df),
        "Total columns": len(df.columns),
        "Duplicate rows": int(df.duplicated().sum()),
        "Total missing values": int(missing.sum()),
        "Columns with missing values": int(
            (missing > 0).sum()
        ),
        "Missing values by column": missing[
            missing > 0
        ].to_dict(),
        "Missing percentage by column": missing_percent[
            missing > 0
        ].to_dict(),
    }