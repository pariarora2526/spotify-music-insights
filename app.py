
import streamlit as st

from data_utils import load_tracks
from table_view import render_track_explorer

st.set_page_config(
    page_title="Spotify Music Insights",
    page_icon="🎵",
    layout="wide"
)

@st.cache_data
def load_data():
    return load_tracks()

df = load_data()

st.title("🎵 Spotify Music Insights")
st.write("Explore tracks, artists, genres, and audio features.")

filtered_df = render_track_explorer(df)

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

st.download_button(
    "Download filtered data as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="spotify_tracks_filtered.csv",
    mime="text/csv"
)
