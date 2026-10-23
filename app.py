
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Spotify Music Insights",
    page_icon="🎵",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/spotify_tracks.csv")
    return df.drop(columns=["Unnamed: 0"], errors="ignore")

df = load_data()

st.title("🎵 Spotify Music Insights")
st.write("Explore tracks, artists, genres, and audio features.")

# Sidebar filters
st.sidebar.header("Filters")

genres = sorted(df["track_genre"].dropna().unique())
selected_genres = st.sidebar.multiselect(
    "Choose genres",
    genres,
    default=genres[:5]
)

filtered_df = df[df["track_genre"].isin(selected_genres)]

# KPI cards
c1, c2, c3 = st.columns(3)
c1.metric("Tracks", f"{len(filtered_df):,}")
c2.metric(
    "Average Popularity",
    f"{filtered_df['popularity'].mean():.1f}"
    if not filtered_df.empty else "N/A"
)
c3.metric(
    "Unique Artists",
    f"{filtered_df['artists'].nunique():,}"
)

st.subheader("Most Popular Tracks")
top_tracks = filtered_df.nlargest(10, "popularity")
st.dataframe(
    top_tracks[["track_name", "artists", "track_genre", "popularity"]],
    use_container_width=True
)

st.subheader("Popularity Distribution")
st.bar_chart(filtered_df["popularity"].value_counts().sort_index())

st.subheader("Explore the Dataset")
st.dataframe(filtered_df.head(100), use_container_width=True)

st.download_button(
    "Download filtered data as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="spotify_tracks_filtered.csv",
    mime="text/csv"
)
