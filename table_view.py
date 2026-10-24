import math

import pandas as pd
import streamlit as st


DEFAULT_COLUMNS = [
    "track_name",
    "artists",
    "album_name",
    "track_genre",
    "popularity",
    "duration_ms",
    "explicit",
]


DISPLAY_NAMES = {
    "track_name": "Track",
    "artists": "Artist",
    "album_name": "Album",
    "track_genre": "Genre",
    "popularity": "Popularity",
    "duration_ms": "Duration",
    "explicit": "Explicit",
}


def format_duration(value):
    """Convert milliseconds into minutes and seconds."""
    if pd.isna(value):
        return "Unknown"

    total_seconds = int(value / 1000)
    minutes, seconds = divmod(total_seconds, 60)

    return f"{minutes}:{seconds:02d}"


def render_track_explorer(df):
    """Render search, filters, sorting, and pagination."""

    st.sidebar.markdown("## 🎧 Explore Music")
    st.sidebar.caption(
        "Search and refine the tracks shown below."
    )

    if st.sidebar.button(
        "↺ Clear filters",
        use_container_width=True,
    ):
        for key in (
            "track_search",
            "track_genres",
            "track_popularity",
            "track_explicit",
            "track_columns",
            "track_sort",
            "track_descending",
            "track_page_size",
            "track_page",
        ):
            st.session_state.pop(key, None)

        st.rerun()

    search_text = st.sidebar.text_input(
        "Search tracks, artists, albums, or genres",
        key="track_search",
        placeholder="Try a song or artist...",
    ).strip()

    filtered = df.copy()

    # Search across relevant text columns.
    searchable_columns = [
        column
        for column in (
            "track_name",
            "artists",
            "album_name",
            "track_genre",
        )
        if column in filtered.columns
    ]

    if search_text and searchable_columns:
        searchable_text = (
            filtered[searchable_columns]
            .fillna("")
            .astype(str)
            .agg(" ".join, axis=1)
        )

        filtered = filtered[
            searchable_text.str.contains(
                search_text,
                case=False,
                regex=False,
                na=False,
            )
        ]

    # Genre filter.
    if "track_genre" in filtered.columns:
        genres = sorted(
            df["track_genre"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_genres = st.sidebar.multiselect(
            "🎼 Genres",
            options=genres,
            default=genres,
            key="track_genres",
        )

        filtered = filtered[
            filtered["track_genre"].isin(selected_genres)
        ]

    # Popularity filter with a stable range.
    if "popularity" in df.columns:
        valid_popularity = pd.to_numeric(
            df["popularity"], errors="coerce"
        ).dropna()

        if not valid_popularity.empty:
            low = max(0, int(valid_popularity.min()))
            high = min(100, int(valid_popularity.max()))

            if low < high:
                selected_range = st.sidebar.slider(
                    "⭐ Popularity range",
                    min_value=low,
                    max_value=high,
                    value=(low, high),
                    key="track_popularity",
                )

                popularity_values = pd.to_numeric(
                    filtered["popularity"],
                    errors="coerce",
                )

                filtered = filtered[
                    popularity_values.between(
                        selected_range[0],
                        selected_range[1],
                    )
                ]

    # Explicit-content filter.
    if "explicit" in filtered.columns:
        explicit_filter = st.sidebar.selectbox(
            "Content type",
            [
                "All tracks",
                "Explicit only",
                "Non-explicit only",
            ],
            key="track_explicit",
        )

        explicit_values = (
            filtered["explicit"]
            .astype("string")
            .str.lower()
            .map({
                "true": True,
                "false": False,
                "1": True,
                "0": False,
            })
        )

        if explicit_filter == "Explicit only":
            filtered = filtered[explicit_values == True]
        elif explicit_filter == "Non-explicit only":
            filtered = filtered[explicit_values == False]

    st.markdown("### 🎵 Track Explorer")
    st.caption(
        "Find a track, compare popularity, and explore the collection."
    )

    available_columns = [
        column
        for column in DEFAULT_COLUMNS
        if column in filtered.columns
    ]

    if not available_columns:
        st.info("No recognized track columns are available.")
        return filtered

    default_columns = [
        column
        for column in available_columns
        if column != "duration_ms"
    ]

    if "duration_ms" in available_columns:
        default_columns.append("duration_ms")

    selected_columns = st.multiselect(
        "Visible columns",
        options=available_columns,
        default=default_columns,
        format_func=lambda col: DISPLAY_NAMES.get(col, col.title()),
        key="track_columns",
    )

    if not selected_columns:
        st.info("Select at least one column to display.")
        return filtered

    sort_column, order_column, size_column = st.columns(
        [2, 1, 1]
    )

    sort_by = sort_column.selectbox(
        "Sort by",
        options=selected_columns,
        format_func=lambda col: DISPLAY_NAMES.get(col, col.title()),
        key="track_sort",
    )

    descending = order_column.checkbox(
        "Descending",
        value=True,
        key="track_descending",
    )

    rows_per_page = size_column.selectbox(
        "Rows per page",
        options=[25, 50, 100, 250],
        key="track_page_size",
    )

    sorted_tracks = filtered.sort_values(
        by=sort_by,
        ascending=not descending,
        na_position="last",
    )

    total_rows = len(sorted_tracks)

    page_count = max(
        1,
        math.ceil(total_rows / rows_per_page),
    )

    if st.session_state.get("track_page", 1) > page_count:
        st.session_state["track_page"] = page_count

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=page_count,
        value=st.session_state.get("track_page", 1),
        step=1,
        key="track_page",
    )

    start = (int(page) - 1) * rows_per_page

    visible_tracks = sorted_tracks.iloc[
        start:start + rows_per_page
    ]

    st.caption(
        f"Showing {len(visible_tracks):,} of "
        f"{total_rows:,} matching tracks"
    )

    if visible_tracks.empty:
        st.info("No tracks match your current filters.")
        return filtered

    # Format a copy for display, not the underlying data.
    display_df = visible_tracks[selected_columns].copy()

    for column in (
        "track_name",
        "artists",
        "album_name",
        "track_genre",
    ):
        if column in display_df.columns:
            display_df[column] = (
                display_df[column]
                .fillna("Unknown")
                .replace("", "Unknown")
            )

    if "duration_ms" in display_df.columns:
        display_df["duration_ms"] = (
            display_df["duration_ms"].map(format_duration)
        )

    display_df = display_df.rename(
        columns={
            column: DISPLAY_NAMES.get(column, column.title())
            for column in display_df.columns
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=430,
    )

    return filtered