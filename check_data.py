import pandas as pd

df = pd.read_csv("data/spotify_tracks.csv")

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())