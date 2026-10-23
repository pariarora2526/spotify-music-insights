
import pandas as pd

from analytics import (
    get_total_tracks,
    get_total_artists,
    get_average_popularity,
    get_top_tracks,
    get_top_artists,
    get_genre_counts,
)


df = pd.read_csv("data/spotify_tracks.csv")

print("Total tracks:", get_total_tracks(df))
print("Unique artist entries:", get_total_artists(df))
print("Average popularity:", get_average_popularity(df))
print("\nTop tracks:")
print(get_top_tracks(df))
print("\nTop artists:")
print(get_top_artists(df))
print("\nGenre counts:")
print(get_genre_counts(df).head())
