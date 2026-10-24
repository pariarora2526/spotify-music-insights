import streamlit as st
import pandas as pd
import plotly.express as px

from data_utils import load_tracks, get_data_quality_report
from table_view import render_track_explorer, format_duration


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SoundScape | Spotify Insights",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM DARK THEME
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    .stApp {
        background-color: #0b0f0e;
        color: #f4f7f5;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #111714;
        border-right: 1px solid #26352c;
    }

    [data-testid="stSidebar"] h2 {
        color: #65e69a;
    }

    .hero {
        background: linear-gradient(
            120deg,
            #142b20 0%,
            #183d2b 48%,
            #10251c 100%
        );
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #315840;
        margin-bottom: 24px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #c1d8c8;
        font-size: 15px;
        line-height: 1.7;
    }

    .hero-tag {
        color: #6bed9d;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #19231d,
            #121915
        );
        border: 1px solid #2a3b30;
        border-radius: 16px;
        padding: 20px;
        min-height: 120px;
    }

    div[data-testid="stMetricLabel"] {
        color: #b5c7bb;
        font-size: 13px;
    }

    div[data-testid="stMetricValue"] {
        color: #65e69a;
        font-weight: 800;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 12px;
    }

    h1, h2, h3 {
        color: #f5f8f6;
    }

    h2 {
        font-weight: 700;
    }

    [data-testid="stPlotlyChart"] {
        background: #111714;
        border: 1px solid #25362b;
        border-radius: 16px;
        padding: 8px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #2a3b30;
        border-radius: 12px;
        overflow: hidden;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    div.stDownloadButton > button {
        background-color: #1db954;
        color: #07110a;
        border: none;
    }

    div.stDownloadButton > button:hover {
        background-color: #65e69a;
        color: #07110a;
    }

    hr {
        border-color: #29382e;
    }

    .section-caption {
        color: #94a99a;
        font-size: 13px;
        margin-top: -8px;
        margin-bottom: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return load_tracks()


try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load the Spotify dataset: {error}")
    st.info(
        "Check that data/spotify_tracks.csv exists "
        "inside your project folder."
    )
    st.stop()


if df.empty:
    st.warning("The dataset contains no tracks.")
    st.stop()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">YOUR MUSIC. YOUR DATA. YOUR DISCOVERIES.</div>
        <div class="hero-title">🎧 SoundScape</div>
        <div class="hero-subtitle">
            An interactive Spotify analytics experience.
            Discover popular tracks, compare genres, explore audio
            features, and uncover patterns across the music library.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# TRACK EXPLORER AND FILTERS
# --------------------------------------------------

filtered_df = render_track_explorer(df)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.markdown("---")
st.subheader("📊 Music at a Glance")
st.caption(
    "These metrics update automatically when you change your filters."
)

total_tracks = len(filtered_df)

if "popularity" in filtered_df.columns:
    average_popularity = pd.to_numeric(
        filtered_df["popularity"],
        errors="coerce",
    ).mean()
else:
    average_popularity = float("nan")

if "artists" in filtered_df.columns:
    unique_artists = filtered_df["artists"].nunique()
else:
    unique_artists = 0

if "track_genre" in filtered_df.columns:
    unique_genres = filtered_df["track_genre"].nunique()
else:
    unique_genres = 0

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "🎵 Matching Tracks",
    f"{total_tracks:,}",
)

k2.metric(
    "⭐ Avg. Popularity",
    (
        f"{average_popularity:.1f}/100"
        if pd.notna(average_popularity)
        else "N/A"
    ),
)

k3.metric(
    "🎤 Unique Artists",
    f"{unique_artists:,}",
)

k4.metric(
    "🎼 Genres",
    f"{unique_genres:,}",
)


# --------------------------------------------------
# EMPTY FILTER RESULT CHECK
# --------------------------------------------------

if filtered_df.empty:
    st.warning(
        "No tracks match these filters. "
        "Try changing your search or clearing the filters."
    )
    st.stop()


# --------------------------------------------------
# PREPARE CHART DATA
# --------------------------------------------------

chart_df = filtered_df.copy()

if "popularity" in chart_df.columns:
    chart_df["popularity"] = pd.to_numeric(
        chart_df["popularity"],
        errors="coerce",
    )

chart_df = chart_df.dropna(
    subset=["popularity"]
) if "popularity" in chart_df.columns else chart_df


# --------------------------------------------------
# CHART 1: POPULARITY DISTRIBUTION
# --------------------------------------------------

st.markdown("---")
st.subheader("📈 Popularity & Genre Insights")
st.caption(
    "Understand how popularity is distributed and which genres "
    "appear most frequently in the filtered collection."
)

chart_left, chart_right = st.columns(2)

with chart_left:
    st.markdown("#### Popularity Distribution")

    if (
        "popularity" in chart_df.columns
        and not chart_df.empty
    ):
        popularity_fig = px.histogram(
            chart_df,
            x="popularity",
            nbins=20,
            color_discrete_sequence=["#1ed760"],
            labels={
                "popularity": "Popularity score",
                "count": "Number of tracks",
            },
        )

        popularity_fig.update_layout(
            template="plotly_dark",
            height=350,
            margin=dict(l=20, r=20, t=25, b=35),
            paper_bgcolor="#111714",
            plot_bgcolor="#111714",
            showlegend=False,
        )

        popularity_fig.update_xaxes(
            gridcolor="#26352c",
            zeroline=False,
        )

        popularity_fig.update_yaxes(
            gridcolor="#26352c",
            zeroline=False,
        )

        st.plotly_chart(
            popularity_fig,
            use_container_width=True,
        )
    else:
        st.info("Popularity data is unavailable.")


# --------------------------------------------------
# CHART 2: TOP GENRES
# --------------------------------------------------

with chart_right:
    st.markdown("#### Top 10 Genres by Track Count")

    if "track_genre" in filtered_df.columns:
        genre_counts = (
            filtered_df["track_genre"]
            .dropna()
            .value_counts()
            .head(10)
            .reset_index()
        )

        genre_counts.columns = ["Genre", "Tracks"]

        if not genre_counts.empty:
            genre_fig = px.bar(
                genre_counts.sort_values("Tracks"),
                x="Tracks",
                y="Genre",
                orientation="h",
                color="Tracks",
                color_continuous_scale=[
                    "#173d29",
                    "#1db954",
                    "#8bf5b0",
                ],
                labels={
                    "Tracks": "Number of tracks",
                    "Genre": "Genre",
                },
            )

            genre_fig.update_layout(
                template="plotly_dark",
                height=350,
                margin=dict(l=10, r=20, t=20, b=35),
                paper_bgcolor="#111714",
                plot_bgcolor="#111714",
                coloraxis_showscale=False,
            )

            genre_fig.update_xaxes(
                gridcolor="#26352c",
                zeroline=False,
            )

            genre_fig.update_yaxes(
                gridcolor="#111714",
                zeroline=False,
            )

            st.plotly_chart(
                genre_fig,
                use_container_width=True,
            )
        else:
            st.info("No genre information is available.")
    else:
        st.info("The dataset does not contain a genre column.")


# --------------------------------------------------
# CHART 3: AUDIO FEATURES
# --------------------------------------------------

st.markdown("---")
st.subheader("🎚️ Audio Feature Profile")
st.caption(
    "Compare average audio-feature values for the selected tracks. "
    "Feature values are shown on a 0–1 scale."
)

audio_features = [
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
]

available_features = [
    feature
    for feature in audio_features
    if feature in filtered_df.columns
]

if available_features:
    audio_data = []

    for feature in available_features:
        values = pd.to_numeric(
            filtered_df[feature],
            errors="coerce",
        )

        average = values.mean()

        if pd.notna(average):
            audio_data.append({
                "Feature": feature.replace("_", " ").title(),
                "Average Value": round(float(average), 3),
            })

    if audio_data:
        audio_df = pd.DataFrame(audio_data)

        audio_fig = px.bar(
            audio_df,
            x="Feature",
            y="Average Value",
            color="Average Value",
            color_continuous_scale=[
                "#173d29",
                "#1db954",
                "#8bf5b0",
            ],
            text="Average Value",
            labels={
                "Feature": "Audio feature",
                "Average Value": "Average (0–1)",
            },
        )

        audio_fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            cliponaxis=False,
        )

        audio_fig.update_layout(
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=25, t=25, b=40),
            paper_bgcolor="#111714",
            plot_bgcolor="#111714",
            coloraxis_showscale=False,
            yaxis_range=[
                0,
                min(
                    1.15,
                    max(
                        0.2,
                        float(audio_df["Average Value"].max()) + 0.12,
                    ),
                ),
            ],
        )

        audio_fig.update_yaxes(
            gridcolor="#26352c",
            zeroline=False,
        )

        st.plotly_chart(
            audio_fig,
            use_container_width=True,
        )
    else:
        st.info("No valid audio-feature values are available.")
else:
    st.info("Audio-feature columns were not found.")


# --------------------------------------------------
# TOP POPULAR TRACKS
# --------------------------------------------------

st.markdown("---")
st.subheader("🔥 Most Popular Tracks")
st.caption(
    "The highest-popularity tracks matching your current filters."
)

if "popularity" in filtered_df.columns:
    top_tracks = filtered_df.copy()

    top_tracks["popularity"] = pd.to_numeric(
        top_tracks["popularity"],
        errors="coerce",
    )

    top_tracks = (
        top_tracks.dropna(subset=["popularity"])
        .nlargest(10, "popularity")
    )

    if not top_tracks.empty:
        top_columns = [
            column
            for column in [
                "track_name",
                "artists",
                "album_name",
                "track_genre",
                "popularity",
                "duration_ms",
            ]
            if column in top_tracks.columns
        ]

        top_display = top_tracks[top_columns].copy()

        # Make missing names readable.
        for column in (
            "track_name",
            "artists",
            "album_name",
            "track_genre",
        ):
            if column in top_display.columns:
                top_display[column] = (
                    top_display[column]
                    .fillna("Unknown")
                )

        # Format durations for display.
        if "duration_ms" in top_display.columns:
            top_display["duration_ms"] = (
                top_display["duration_ms"].map(format_duration)
            )

        top_display = top_display.rename(
            columns={
                "track_name": "Track",
                "artists": "Artist",
                "album_name": "Album",
                "track_genre": "Genre",
                "popularity": "Popularity",
                "duration_ms": "Duration",
            }
        )

        st.dataframe(
            top_display,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No valid popularity scores are available.")
else:
    st.info("Popularity data is unavailable.")


# --------------------------------------------------
# CSV DOWNLOAD
# --------------------------------------------------

st.markdown("---")
st.subheader("📥 Export Your Data")
st.caption(
    "Download the filtered dataset for further analysis in Excel, "
    "Python, or Power BI."
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="⬇️ Download Filtered Tracks (CSV)",
    data=csv_data,
    file_name="soundscape_filtered_tracks.csv",
    mime="text/csv",
)


# --------------------------------------------------
# DATA QUALITY REPORT
# --------------------------------------------------

with st.expander("🧹 Dataset Quality Report"):
    report = get_data_quality_report(df)

    q1, q2, q3 = st.columns(3)

    q1.metric(
        "Cleaned Rows",
        f"{report['Total rows']:,}",
    )

    q2.metric(
        "Missing Values",
        f"{report['Total missing values']:,}",
    )

    q3.metric(
        "Exact Duplicate Rows",
        f"{report['Duplicate rows']:,}",
    )

    st.write(
        f"**Columns:** {report['Total columns']}"
    )

    st.write(
        f"**Columns containing missing values:** "
        f"{report['Columns with missing values']}"
    )

    missing_counts = report["Missing values by column"]

    if missing_counts:
        missing_df = pd.DataFrame(
            [
                {
                    "Column": column,
                    "Missing Values": count,
                    "Missing Percentage": (
                        report["Missing percentage by column"][column]
                    ),
                }
                for column, count in missing_counts.items()
            ]
        )

        st.dataframe(
            missing_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No missing values were detected.")

    st.caption(
        "The report describes the cleaned dataset. Missing values "
        "are not replaced with invented data, and the original CSV "
        "is not overwritten."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        color: #8da394;
        padding: 18px 0 10px 0;
        font-size: 12px;
    ">
        <strong style="color: #65e69a;">SOUNDSCAPE</strong>
        &nbsp; · &nbsp; Spotify Music Intelligence
        <br><br>
        Built with Python, Streamlit, Pandas and Plotly
    </div>
    """,
    unsafe_allow_html=True,
)