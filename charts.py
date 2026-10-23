
import plotly.express as px


def popularity_chart(df):
    """Bar chart of the top 10 tracks by popularity."""
    top_tracks = df.nlargest(10, "popularity").copy()
    top_tracks["display_name"] = (
        top_tracks["track_name"].fillna("Unknown").str.slice(0, 35)
    )

    return px.bar(
        top_tracks.sort_values("popularity"),
        x="popularity",
        y="display_name",
        orientation="h",
        color="popularity",
        hover_data=["artists", "track_genre"],
        title="Top 10 Tracks by Popularity",
        labels={
            "popularity": "Popularity Score",
            "display_name": "Track",
        },
    )


def artist_chart(df):
    """Bar chart of artists with the highest average popularity."""
    top_artists = (
        df.groupby("artists", dropna=True)["popularity"]
        .mean()
        .nlargest(10)
        .reset_index()
        .sort_values("popularity")
    )

    return px.bar(
        top_artists,
        x="popularity",
        y="artists",
        orientation="h",
        title="Top 10 Artists by Average Popularity",
        labels={
            "popularity": "Average Popularity",
            "artists": "Artist",
        },
    )


def genre_chart(df):
    """Show the number of tracks in each genre."""
    genre_counts = df["track_genre"].value_counts().reset_index()
    genre_counts.columns = ["track_genre", "track_count"]

    return px.bar(
        genre_counts,
        x="track_genre",
        y="track_count",
        title="Number of Tracks by Genre",
        labels={
            "track_genre": "Genre",
            "track_count": "Number of Tracks",
        },
    )


def danceability_energy_chart(df):
    """Compare danceability and energy."""
    return px.scatter(
        df,
        x="danceability",
        y="energy",
        color="track_genre",
        hover_data=["track_name", "artists"],
        title="Danceability vs Energy",
        labels={
            "danceability": "Danceability",
            "energy": "Energy",
        },
    )


def popularity_distribution_chart(df):
    """Show the distribution of popularity scores."""
    return px.histogram(
        df,
        x="popularity",
        nbins=30,
        title="Distribution of Track Popularity",
        labels={"popularity": "Popularity Score"},
    )
