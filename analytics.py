
import pandas as pd


def get_total_tracks(df):
    """Return the total number of tracks."""
    return len(df)


def get_total_artists(df):
    """Return the number of unique artist entries."""
    return df["artists"].nunique()


def get_average_popularity(df):
    """Return the average popularity score."""
    return round(df["popularity"].mean(), 2)


def get_top_tracks(df, n=10):
    """Return the most popular tracks."""
    columns = ["track_name", "artists", "popularity"]

    return (
        df.sort_values("popularity", ascending=False)[columns]
        .head(n)
        .reset_index(drop=True)
    )


def get_top_artists(df, n=10):
    """Return artists with the highest average popularity."""
    return (
        df.groupby("artists")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(n)
        .reset_index(name="average_popularity")
    )


def get_genre_counts(df):
    """Return the number of tracks in each genre."""
    return (
        df["track_genre"]
        .value_counts()
        .rename_axis("track_genre")
        .reset_index(name="track_count")
    )
