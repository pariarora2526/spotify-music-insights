import html

import pandas as pd
import plotly.express as px
import streamlit as st

from data_utils import load_tracks
from table_view import render_track_explorer


st.set_page_config(
    page_title="SoundScape | Music Intelligence",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------- DATA ----------
@st.cache_data
def load_data():
    return load_tracks()


df = load_data()


def numeric_col(data, name):
    if name not in data.columns:
        return pd.Series(index=data.index, dtype="float64")
    return pd.to_numeric(data[name], errors="coerce")


def safe_text(value):
    if pd.isna(value) or str(value).strip() == "":
        return "Unknown"
    return str(value).strip()


def duration_text(value):
    if pd.isna(value) or value <= 0:
        return "—"
    seconds = int(value / 1000)
    return f"{seconds // 60}:{seconds % 60:02d}"


def chart_style(fig, height=340):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=10, r=15, t=22, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color="#c7cbd1", size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c7cbd1")),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.07)", zerolinecolor="rgba(255,255,255,0.08)")
    return fig


# ---------- VISUAL SYSTEM ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
      --green: #1ed760;
      --bg: #080808;
      --surface: #171717;
      --surface2: #202020;
      --muted: #a7a7a7;
      --line: rgba(255,255,255,.08);
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #080808; color: #f5f5f5; }
    [data-testid="stHeader"] { background: rgba(8,8,8,.96); }
    .block-container { max-width: 1700px; padding-top: 1rem; padding-bottom: 2.8rem; }
    [data-testid="stSidebar"] { background: #121212; border-right: 1px solid #242424; }
    [data-testid="stSidebar"] > div { padding-top: 1.1rem; }
    [data-testid="stSidebar"] * { color: #eeeeee; }
    h1,h2,h3 { font-family: 'Space Grotesk', sans-serif !important; color: #f7f7f7 !important; letter-spacing: -.45px; }
    h1 { font-size: clamp(1.9rem, 3vw, 2.65rem) !important; font-weight: 700 !important; }
    h2 { font-size: 1.55rem !important; font-weight: 700 !important; }
    h3 { font-size: 1.1rem !important; font-weight: 700 !important; }
    p, label, .stCaption { color: #b3b3b3; }
    [data-testid="stMetric"] { background: linear-gradient(145deg,#202020,#151515); border: 1px solid #303030; border-radius: 16px; padding: 18px 19px; box-shadow: 0 8px 18px rgba(0,0,0,.22), inset 0 1px rgba(255,255,255,.04); }
    [data-testid="stMetricLabel"] { color: #b3b3b3 !important; font-size: .85rem !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'Space Grotesk',sans-serif; font-size: 1.8rem !important; font-weight: 700; }
    [data-testid="stMetricDelta"] { color: var(--green) !important; }
    .brand { display:flex; align-items:center; gap:10px; padding: 0.25rem 0 1.2rem; }
    .brand-mark { width:38px; height:38px; border-radius:50%; background:var(--green); color:#050505; display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:800; }
    .brand-name { font-family:'Space Grotesk',sans-serif; font-size:1.28rem; font-weight:800; letter-spacing:-.6px; }
    .brand-name span { color:var(--green); }
    .side-label { color:#777 !important; text-transform:uppercase; letter-spacing:1.6px; font-size:.69rem; font-weight:800; margin:1rem 0 .45rem; }
    .side-note { background:#202020; border-radius:12px; padding:14px; color:#aaa; font-size:.8rem; line-height:1.55; margin-top:1rem; }
    .topline { display:flex; justify-content:space-between; align-items:center; gap:1rem; padding: .2rem 0 1rem; border-bottom:1px solid #242424; margin-bottom:1.5rem; }
    .top-kicker { color:#a7a7a7; font-size:.77rem; letter-spacing:1.7px; font-weight:700; text-transform:uppercase; }
    .hero { border-radius:18px; overflow:hidden; padding: 28px 30px; min-height:210px; border:1px solid rgba(255,255,255,.08); background: radial-gradient(ellipse at 85% 15%,rgba(30,215,96,.27),transparent 30%), radial-gradient(ellipse at 65% 120%,rgba(113,66,180,.30),transparent 42%), linear-gradient(120deg,#262626,#171717 65%,#211b29); box-shadow:0 16px 36px rgba(0,0,0,.28), inset 0 1px rgba(255,255,255,.06); }
    .hero-label { font-size:.72rem; color:#1ed760; letter-spacing:2px; font-weight:800; text-transform:uppercase; margin-bottom:10px; }
    .hero-title { font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,3.3vw,3.1rem); line-height:1.08; color:white; font-weight:700; letter-spacing:-1.3px; }
    .hero-copy { color:#c0c0c0; max-width:640px; margin-top:12px; line-height:1.6; font-size:.95rem; }
    .hero-art { height:170px; border-radius:16px; background:linear-gradient(145deg,#2e5c40,#1ed760 48%,#7c45a5 100%); display:flex; align-items:center; justify-content:center; box-shadow:0 16px 32px rgba(0,0,0,.25),inset 0 1px rgba(255,255,255,.25); position:relative; overflow:hidden; }
    .hero-art:before,.hero-art:after { content:""; position:absolute; border:1px solid rgba(255,255,255,.3); border-radius:50%; width:160px; height:160px; }
    .hero-art:after { width:110px; height:110px; }
    .disc { width:76px; height:76px; border-radius:50%; background:radial-gradient(circle,#101010 0 10%,#ddd 11% 13%,#111 14% 100%); z-index:1; box-shadow:0 0 0 14px rgba(0,0,0,.14),0 0 0 28px rgba(0,0,0,.1); }
    .section-head { margin:1.8rem 0 .3rem; font-family:'Space Grotesk',sans-serif; font-size:1.45rem; font-weight:700; color:#f5f5f5; }
    .section-sub { color:#999; font-size:.87rem; margin-bottom:1rem; }
    .panel-title { font-size:1rem; font-weight:700; color:#f5f5f5; margin-bottom:2px; }
    .panel-sub { font-size:.78rem; color:#969696; margin-bottom:10px; }
    .music-card { background:linear-gradient(145deg,#242424,#171717); border:1px solid #2c2c2c; padding:12px; border-radius:13px; height:100%; box-shadow:0 8px 16px rgba(0,0,0,.15); transition:transform .18s ease,background .18s ease; }
    .music-card:hover { transform:translateY(-3px); background:#292929; }
    .cover { width:100%; aspect-ratio:1/1; border-radius:9px; display:flex; align-items:center; justify-content:center; overflow:hidden; margin-bottom:12px; position:relative; }
    .cover span { font-family:'Space Grotesk',sans-serif; font-size:2.5rem; font-weight:700; color:rgba(255,255,255,.9); text-shadow:0 3px 18px rgba(0,0,0,.3); }
    .track-name { font-size:.91rem; font-weight:700; color:#f5f5f5; line-height:1.35; margin-bottom:5px; overflow-wrap:anywhere; }
    .track-artist { color:#a7a7a7; font-size:.78rem; line-height:1.45; overflow-wrap:anywhere; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid #282828; }
    .stTabs [data-baseweb="tab"] { background:transparent; border-radius:8px 8px 0 0; color:#a7a7a7; padding:10px 15px; }
    .stTabs [aria-selected="true"] { color:#1ed760 !important; border-bottom:2px solid #1ed760 !important; }
    div[data-testid="stPlotlyChart"],div[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }
    div[data-testid="stDownloadButton"] button { background:#1ed760; color:#050505; border:0; border-radius:24px; padding:.55rem 1.2rem; font-weight:800; }
    div[data-testid="stDownloadButton"] button:hover { background:#3be477; color:#050505; }
    .stButton button { border-radius:24px; }
    hr { border-color:#292929; }
    #MainMenu, footer { visibility:hidden; }
    @media(max-width:760px) { .hero { padding:22px; } .hero-art { height:125px; } .topline { align-items:flex-start; flex-direction:column; } }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-mark">≋</div>
          <div class="brand-name">Sound<span>Scape</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-label">Workspace</div>', unsafe_allow_html=True)
    st.caption("Music overview")
    st.caption("Genre discovery")
    st.caption("Artist insights")
    st.caption("Audio features")
    st.caption("Track explorer")
    st.markdown('<div class="side-label">Your dataset</div>', unsafe_allow_html=True)
    st.write(f"**{len(df):,}** tracks")
    st.write(f"**{df['track_genre'].nunique():,}** genres" if "track_genre" in df.columns else "Genre data unavailable")
    st.markdown(
        """
        <div class="side-note">
          <strong style="color:#eee">Music, made meaningful.</strong><br>
          Explore the tracks, artists and audio features in your dataset.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- TOP BAR + HERO ----------
st.markdown(
    """
    <div class="topline">
      <div class="top-kicker">Music intelligence platform</div>
      <div style="color:#888;font-size:.82rem">Dataset overview&nbsp;&nbsp; / &nbsp;&nbsp;Analytics</div>
    </div>
    """,
    unsafe_allow_html=True,
)

hero_left, hero_right = st.columns([1.65, .75], vertical_alignment="center")
with hero_left:
    st.markdown(
        """
        <div class="hero">
          <div class="hero-label">SoundScape · Explore your music</div>
          <div class="hero-title">Your music.<br>In a new light.</div>
          <div class="hero-copy">
            Discover the artists, genres and audio characteristics behind
            your collection. Explore the data, find patterns and see music differently.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with hero_right:
    st.markdown('<div class="hero-art"><div class="disc"></div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-head">Your library at a glance</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">A live snapshot calculated from your dataset.</div>', unsafe_allow_html=True)

avg_pop = numeric_col(df, "popularity").mean()
avg_energy = numeric_col(df, "energy").mean()
artist_count = df["artists"].dropna().nunique() if "artists" in df.columns else 0
genre_count = df["track_genre"].dropna().nunique() if "track_genre" in df.columns else 0

m1, m2, m3, m4 = st.columns(4, gap="medium")
m1.metric("Tracks in library", f"{len(df):,}")
m2.metric("Artist entries", f"{artist_count:,}")
m3.metric("Genres", f"{genre_count:,}")
m4.metric("Average popularity", f"{avg_pop:.1f} / 100" if pd.notna(avg_pop) else "—")

# A clear musical collection row, using the real data and generated CSS covers.
st.markdown('<div class="section-head">Popular in your collection</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Tracks with the highest popularity scores in the dataset.</div>', unsafe_allow_html=True)

if not df.empty and "popularity" in df.columns:
    popular = df.copy()
    popular["_popularity"] = numeric_col(popular, "popularity")
    popular = popular.dropna(subset=["_popularity"]).nlargest(6, "_popularity")
    palettes = [
        "linear-gradient(145deg,#284f3b,#1ed760)",
        "linear-gradient(145deg,#43264f,#bb86fc)",
        "linear-gradient(145deg,#24495d,#50d6e8)",
        "linear-gradient(145deg,#6b303d,#fa709a)",
        "linear-gradient(145deg,#6c4d23,#f6bd60)",
        "linear-gradient(145deg,#303b63,#818cf8)",
    ]
    card_cols = st.columns(6, gap="medium")
    for i, (_, track) in enumerate(popular.iterrows()):
        track_name = safe_text(track.get("track_name", "Unknown"))
        artist = safe_text(track.get("artists", "Unknown"))
        genre = safe_text(track.get("track_genre", "Unknown"))
        with card_cols[i]:
            st.markdown(
                f"""
                <div class="music-card">
                  <div class="cover" style="background:{palettes[i % len(palettes)]}">
                    <span>{html.escape(track_name[:1].upper())}</span>
                  </div>
                  <div class="track-name">{html.escape(track_name)}</div>
                  <div class="track-artist">{html.escape(artist)}</div>
                  <div style="color:#1ed760;font-size:.75rem;font-weight:700;margin-top:8px">
                    Popularity {track['_popularity']:.0f}
                  </div>
                  <div style="color:#777;font-size:.72rem;margin-top:3px">{html.escape(genre)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info("No track popularity data is available.")

# ---------- MAIN ANALYTICS ----------
overview_tab, genre_tab, artist_tab, audio_tab, explorer_tab = st.tabs(
    ["Overview", "Genre discovery", "Artist insights", "Audio features", "Track explorer"]
)

with overview_tab:
    st.markdown('<div class="section-head">The listening landscape</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Understand the distribution and characteristics of the collection.</div>', unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown('<div class="panel-title">Popularity distribution</div><div class="panel-sub">Track counts by popularity score</div>', unsafe_allow_html=True)
        pop = numeric_col(df, "popularity").dropna()
        if not pop.empty:
            fig = px.histogram(
                x=pop, nbins=24,
                labels={"x": "Popularity score", "count": "Tracks"},
                color_discrete_sequence=["#1ed760"],
            )
            fig.update_traces(marker_line_color="#0b0b0b", marker_line_width=1)
            fig.update_xaxes(range=[0, 100], title="Popularity score")
            fig.update_yaxes(title="Number of tracks")
            st.plotly_chart(chart_style(fig), width="stretch")
        else:
            st.info("Popularity values are unavailable.")

    with right:
        st.markdown('<div class="panel-title">Average audio profile</div><div class="panel-sub">Average values of key audio features</div>', unsafe_allow_html=True)
        features = ["Energy", "Danceability", "Valence", "Acousticness"]
        cols = ["energy", "danceability", "valence", "acousticness"]
        vals = [numeric_col(df, c).mean() for c in cols]
        feature_df = pd.DataFrame({"Feature": features, "Average score": vals}).dropna()
        if not feature_df.empty:
            fig = px.bar(
                feature_df.sort_values("Average score"),
                x="Average score", y="Feature", orientation="h",
                color="Feature",
                color_discrete_sequence=["#1ed760", "#a78bfa", "#67e8f9", "#fb7185"],
                text=feature_df.sort_values("Average score")["Average score"].map(lambda x: f"{x:.2f}"),
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_xaxes(range=[0, 1], title="Average score")
            fig.update_layout(showlegend=False)
            st.plotly_chart(chart_style(fig), width="stretch")
        else:
            st.info("Audio feature data is unavailable.")

    left2, right2 = st.columns(2, gap="large")
    with left2:
        st.markdown('<div class="panel-title">Largest genres</div><div class="panel-sub">The most represented genres in your dataset</div>', unsafe_allow_html=True)
        if "track_genre" in df.columns:
            counts = df["track_genre"].dropna().value_counts().head(12).sort_values().rename_axis("Genre").reset_index(name="Tracks")
            fig = px.bar(counts, x="Tracks", y="Genre", orientation="h", color="Tracks", color_continuous_scale=["#263d31", "#1ed760"])
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(chart_style(fig, 390), width="stretch")
        else:
            st.info("Genre data is unavailable.")

    with right2:
        st.markdown('<div class="panel-title">Explicit content breakdown</div><div class="panel-sub">Tracks grouped by content label</div>', unsafe_allow_html=True)
        if "explicit" in df.columns:
            labels = df["explicit"].astype("string").str.lower().map({"true":"Explicit", "false":"Non-explicit", "1":"Explicit", "0":"Non-explicit"}).dropna()
            counts = labels.value_counts().rename_axis("Content").reset_index(name="Tracks")
            if not counts.empty:
                fig = px.pie(counts, names="Content", values="Tracks", hole=.62, color="Content", color_discrete_map={"Explicit":"#b69cff", "Non-explicit":"#1ed760"})
                fig.update_traces(textposition="inside", textinfo="label+percent", marker=dict(line=dict(color="#171717", width=3)))
                st.plotly_chart(chart_style(fig, 390), width="stretch")
            else:
                st.info("No explicit-content values available.")
        else:
            st.info("Explicit-content data is unavailable.")

with genre_tab:
    st.markdown('<div class="section-head">Genre discovery</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Explore the balance of genres represented in the collection.</div>', unsafe_allow_html=True)
    if "track_genre" in df.columns:
        genre_counts = df["track_genre"].dropna().value_counts().rename_axis("Genre").reset_index(name="Track count")
        lcol, rcol = st.columns([1.2, 1], gap="large")
        with lcol:
            st.markdown(
                '<div class="panel-title">Interactive genre leaderboard</div>'
                '<div class="panel-sub">Click a bar to explore tracks, popularity and artists in that genre.</div>',
                unsafe_allow_html=True,
            )
            top_genres = genre_counts.head(25).sort_values("Track count")
            genre_palette = [
                "#1ED760", "#A78BFA", "#38BDF8", "#FB7185",
                "#FBBF24", "#2DD4BF", "#F472B6", "#818CF8",
                "#A3E635", "#FB923C", "#E879F9", "#60A5FA",
            ]
            fig = px.bar(
                top_genres,
                x="Track count",
                y="Genre",
                orientation="h",
                color="Genre",
                color_discrete_sequence=genre_palette,
                custom_data=["Track count"],
                labels={"Track count": "Number of tracks", "Genre": "Music genre"},
            )
            fig.update_traces(
                hovertemplate="<b>%{y}</b><br>Tracks: %{x:,}<br><extra>Click to explore</extra>",
                marker_line_width=0,
            )
            fig.update_layout(
                showlegend=False,
                yaxis_title="",
                xaxis_title="Number of tracks",
                clickmode="event+select",
            )
            genre_event = st.plotly_chart(
                chart_style(fig, 650),
                key="interactive_genre_chart",
                on_select="rerun",
                selection_mode="points",
                width="stretch",
            )

            selected_points = genre_event.selection.points
            if selected_points:
                selected_genre = selected_points[0].get("y")
                if selected_genre:
                    genre_tracks = df[
                        df["track_genre"].astype("string") == str(selected_genre)
                    ].copy()
                    st.markdown("---")
                    st.markdown(f"### Exploring: {html.escape(str(selected_genre))}")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Tracks in genre", f"{len(genre_tracks):,}")

                    genre_popularity = numeric_col(genre_tracks, "popularity")
                    c2.metric(
                        "Average popularity",
                        f"{genre_popularity.mean():.1f} / 100" if genre_popularity.notna().any() else "—",
                    )
                    c3.metric(
                        "Unique artist entries",
                        f"{genre_tracks['artists'].nunique():,}" if "artists" in genre_tracks.columns else "—",
                    )

                    st.markdown("#### Most popular tracks in this genre")
                    if "popularity" in genre_tracks.columns:
                        genre_tracks["_popularity_for_display"] = numeric_col(genre_tracks, "popularity")
                        display_cols = [
                            col for col in [
                                "track_name", "artists", "album_name", "popularity",
                                "danceability", "energy", "tempo",
                            ] if col in genre_tracks.columns
                        ]
                        top_tracks = (
                            genre_tracks.dropna(subset=["_popularity_for_display"])
                            .nlargest(10, "_popularity_for_display")
                        )
                        if not top_tracks.empty:
                            st.dataframe(
                                top_tracks[display_cols].reset_index(drop=True),
                                hide_index=True,
                                width="stretch",
                            )
                        else:
                            st.info("Popularity scores are not available for this genre.")
        with rcol:
            st.markdown('<div class="panel-title">Genre share</div>', unsafe_allow_html=True)
            pie_data = genre_counts.head(8).copy()
            if len(genre_counts) > 8:
                pie_data.loc[len(pie_data)] = ["Other genres", int(genre_counts.iloc[8:]["Track count"].sum())]
            fig = px.pie(pie_data, names="Genre", values="Track count", hole=.62, color_discrete_sequence=["#1ed760", "#b69cff", "#67e8f9", "#fb7185", "#fbbf24", "#34d399", "#818cf8", "#f472b6", "#596273"])
            fig.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="#171717", width=3)))
            st.plotly_chart(chart_style(fig, 420), width="stretch")
            st.markdown('<div class="panel-title">Genre data</div>', unsafe_allow_html=True)
            table = genre_counts.copy()
            table["Share of dataset"] = (table["Track count"] / max(len(df), 1) * 100).map(lambda x: f"{x:.2f}%")
            st.dataframe(table, hide_index=True, width="stretch", height=300)
    else:
        st.info("No genre column found in the dataset.")

with artist_tab:
    st.markdown('<div class="section-head">Artist insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Explore artist representation and average track popularity.</div>', unsafe_allow_html=True)
    if "artists" in df.columns:
        artist_data = df.copy()
        artist_data["_popularity"] = numeric_col(artist_data, "popularity")
        artist_data["Artist"] = artist_data["artists"].fillna("Unknown").astype(str)
        artist_summary = artist_data.groupby("Artist", dropna=False).agg(
            Tracks=("Artist", "size"),
            **{"Average popularity": ("_popularity", "mean")}
        ).reset_index()
        lcol, rcol = st.columns(2, gap="large")
        with lcol:
            st.markdown('<div class="panel-title">Artists with the most tracks</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-sub">Click a bar to see tracks by this artist.</div>', unsafe_allow_html=True)
            top_by_tracks = artist_summary.nlargest(15, "Tracks").sort_values("Tracks")
            fig = px.bar(
                top_by_tracks, x="Tracks", y="Artist", orientation="h",
                color="Tracks", color_continuous_scale=["#263d31", "#1ed760"],
                hover_data={"Tracks": True, "Artist": True},
            )
            fig.update_layout(coloraxis_showscale=False, clickmode="event+select")
            tracks_event = st.plotly_chart(
                chart_style(fig, 470), key="artist_tracks_chart",
                on_select="rerun", selection_mode="points", width="stretch",
            )
        with rcol:
            st.markdown('<div class="panel-title">Highest average popularity</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-sub">Click a bar to inspect the artist.</div>', unsafe_allow_html=True)
            top_by_popularity = (
                artist_summary.dropna(subset=["Average popularity"])
                .nlargest(15, "Average popularity").sort_values("Average popularity")
            )
            fig = px.bar(
                top_by_popularity, x="Average popularity", y="Artist", orientation="h",
                color="Average popularity", color_continuous_scale=["#3b2d54", "#b69cff"],
                hover_data={"Tracks": True, "Artist": True, "Average popularity": ":.1f"},
            )
            fig.update_layout(coloraxis_showscale=False, clickmode="event+select")
            fig.update_xaxes(range=[0, 100])
            popularity_event = st.plotly_chart(
                chart_style(fig, 470), key="artist_popularity_chart",
                on_select="rerun", selection_mode="points", width="stretch",
            )

        # Step 1 interaction: selecting a bar reveals matching real tracks.
        selected_artist = None
        if tracks_event.selection.points:
            selected_artist = tracks_event.selection.points[0].get("y")
        if popularity_event.selection.points:
            selected_artist = popularity_event.selection.points[0].get("y") or selected_artist

        if selected_artist:
            selected_artist = str(selected_artist)
            selected_tracks = artist_data[artist_data["Artist"] == selected_artist].copy()
            st.markdown("---")
            st.markdown(f"### 🎤 Exploring: {html.escape(selected_artist)}")
            a1, a2 = st.columns(2)
            a1.metric("Tracks in dataset", f"{len(selected_tracks):,}")
            selected_avg = selected_tracks["_popularity"].mean()
            a2.metric("Average popularity", f"{selected_avg:.1f} / 100" if pd.notna(selected_avg) else "—")
            st.markdown("#### Tracks by this artist")
            selected_tracks = selected_tracks.sort_values("_popularity", ascending=False, na_position="last")
            display_columns = [c for c in ["track_name", "artists", "album_name", "track_genre", "_popularity", "energy", "danceability"] if c in selected_tracks.columns]
            selected_display = selected_tracks[display_columns].head(20).copy()
            if "_popularity" in selected_display.columns:
                selected_display = selected_display.rename(columns={"_popularity": "Popularity"})
            st.dataframe(selected_display, hide_index=True, width="stretch")

        st.markdown('<div class="panel-title">Artist summary</div>', unsafe_allow_html=True)
        artist_summary["Average popularity"] = artist_summary["Average popularity"].round(1)
        st.dataframe(artist_summary.sort_values("Tracks", ascending=False), hide_index=True, width="stretch", height=300)
    else:
        st.info("No artist column found in the dataset.")

with audio_tab:
    st.markdown('<div class="section-head">Audio features</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Compare musical energy, danceability, mood and tempo.</div>', unsafe_allow_html=True)
    lcol, rcol = st.columns(2, gap="large")
    with lcol:
        st.markdown('<div class="panel-title">Energy vs danceability</div>', unsafe_allow_html=True)
        scatter = pd.DataFrame({
            "Danceability": numeric_col(df, "danceability"),
            "Energy": numeric_col(df, "energy"),
            "Popularity": numeric_col(df, "popularity"),
        }).dropna()
        if not scatter.empty:
            if len(scatter) > 3000:
                scatter = scatter.sample(3000, random_state=42)
            fig = px.scatter(scatter, x="Danceability", y="Energy", color="Popularity", color_continuous_scale=["#8b5cf6", "#67e8f9", "#1ed760"], opacity=.7)
            fig.update_traces(marker=dict(size=6))
            fig.update_xaxes(range=[0, 1])
            fig.update_yaxes(range=[0, 1])
            st.plotly_chart(chart_style(fig, 420), width="stretch")
            st.caption("A sample of up to 3,000 tracks is plotted for responsiveness.")
        else:
            st.info("Audio feature values are unavailable.")
    with rcol:
        st.markdown('<div class="panel-title">Tempo distribution</div>', unsafe_allow_html=True)
        tempo = numeric_col(df, "tempo").dropna()
        tempo = tempo[tempo > 0]
        if not tempo.empty:
            fig = px.histogram(x=tempo, nbins=30, labels={"x":"Tempo (BPM)", "count":"Tracks"}, color_discrete_sequence=["#b69cff"])
            fig.update_traces(marker_line_color="#171717", marker_line_width=1)
            fig.update_xaxes(title="Beats per minute")
            fig.update_yaxes(title="Tracks")
            st.plotly_chart(chart_style(fig, 420), width="stretch")
        else:
            st.info("Tempo data is unavailable.")
    st.markdown('<div class="panel-title">Average audio feature scores</div>', unsafe_allow_html=True)
    feature_names = ["Danceability", "Energy", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence"]
    feature_cols = ["danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence"]
    feature_data = pd.DataFrame({"Audio feature": feature_names, "Average score": [numeric_col(df, c).mean() for c in feature_cols]}).dropna().sort_values("Average score")
    if not feature_data.empty:
        fig = px.bar(feature_data, x="Average score", y="Audio feature", orientation="h", color="Audio feature", color_discrete_sequence=["#1ed760", "#b69cff", "#67e8f9", "#fb7185", "#fbbf24", "#34d399", "#818cf8"])
        fig.update_layout(showlegend=False)
        fig.update_xaxes(range=[0, 1])
        st.plotly_chart(chart_style(fig, 380), width="stretch")

with explorer_tab:
    st.markdown('<div class="section-head">Track explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Search, filter, sort and export your music collection.</div>', unsafe_allow_html=True)
    filtered_df = render_track_explorer(df)
    if filtered_df is not None:
        st.markdown('<div class="section-head" style="font-size:1.2rem">Popular tracks in this selection</div>', unsafe_allow_html=True)
        if not filtered_df.empty and "popularity" in filtered_df.columns:
            top = filtered_df.copy()
            top["_pop"] = numeric_col(top, "popularity")
            top = top.dropna(subset=["_pop"]).nlargest(10, "_pop")
            if not top.empty:
                display = pd.DataFrame()
                display["Track"] = top["track_name"].map(safe_text) if "track_name" in top else "Unknown"
                display["Artist"] = top["artists"].map(safe_text) if "artists" in top else "Unknown"
                display["Album"] = top["album_name"].map(safe_text) if "album_name" in top else "Unknown"
                if "duration_ms" in top:
                    display["Duration"] = top["duration_ms"].map(duration_text)
                if "track_genre" in top:
                    display["Genre"] = top["track_genre"].map(safe_text)
                display["Popularity"] = top["_pop"].map(lambda x: f"{x:.0f} / 100")
                if "explicit" in top:
                    display["Content rating"] = top["explicit"].astype("string").str.lower().map({"true":"Explicit","false":"Non-explicit","1":"Explicit","0":"Non-explicit"}).fillna("Unknown")
                st.dataframe(display.reset_index(drop=True), hide_index=True, width="stretch")
            else:
                st.info("No popularity values match the selected filters.")
        else:
            st.info("No tracks match the selected filters.")
        st.download_button(
            "Download filtered tracks (CSV)",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="soundscape_filtered_tracks.csv",
            mime="text/csv",
        )

st.markdown("---")
st.markdown(
    '<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#777;font-size:.76rem"><span>SoundScape · Music Intelligence</span><span>Built with Streamlit, Pandas and Plotly</span><span>Music data, made meaningful.</span></div>',
    unsafe_allow_html=True,
)
