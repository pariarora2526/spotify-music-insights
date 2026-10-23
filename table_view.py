
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


def render_track_explorer(df):
    """Render search, filters, and a paginated track table."""
    st.sidebar.header("Search and filters")

    if st.sidebar.button("Clear filters", use_container_width=True):
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
    ).strip()

    filtered = df.copy()

    searchable_columns = [
        column
        for column in ("track_name", "artists", "album_name", "track_genre")
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
                search_text, case=False, regex=False, na=False
            )
        ]

    if "track_genre" in filtered.columns:
        genres = sorted(
            filtered["track_genre"].dropna().astype(str).unique().tolist()
        )
        selected_genres = st.sidebar.multiselect(
            "Genres",
            options=genres,
            default=genres,
            key="track_genres",
        )
        filtered = filtered[filtered["track_genre"].isin(selected_genres)]

    if "popularity" in filtered.columns:
        popularity = pd.to_numeric(filtered["popularity"], errors="coerce")
        valid_popularity = popularity.dropna()

        if not valid_popularity.empty:
            low = int(valid_popularity.min())
            high = int(valid_popularity.max())

            if low < high:
                selected_range = st.sidebar.slider(
                    "Popularity range",
                    min_value=low,
                    max_value=high,
                    value=(low, high),
                    key="track_popularity",
                )
                filtered = filtered[
                    pd.to_numeric(
                        filtered["popularity"], errors="coerce"
                    ).between(*selected_range)
                ]

    if "explicit" in filtered.columns:
        explicit_filter = st.sidebar.selectbox(
            "Explicit content",
            ["All tracks", "Explicit only", "Non-explicit only"],
            key="track_explicit",
        )

        explicit_values = (
            filtered["explicit"]
            .astype("string")
            .str.lower()
            .map({"true": True, "false": False, "1": True, "0": False})
        )

        if explicit_filter == "Explicit only":
            filtered = filtered[explicit_values == True]
        elif explicit_filter == "Non-explicit only":
            filtered = filtered[explicit_values == False]

    st.subheader("Explore tracks")

    available_columns = [
        column for column in DEFAULT_COLUMNS if column in filtered.columns
    ]

    if not available_columns:
        st.info("No recognized track columns are available to display.")
        return filtered

    selected_columns = st.multiselect(
        "Columns",
        options=available_columns,
        default=available_columns,
        key="track_columns",
    )

    if not selected_columns:
        st.info("Choose at least one column to display the track table.")
        return filtered

    sort_column, sort_order, page_size_column = st.columns([2, 1, 1])

    sort_by = sort_column.selectbox(
        "Sort by",
        options=selected_columns,
        key="track_sort",
    )
    descending = sort_order.checkbox(
        "Descending",
        value=True,
        key="track_descending",
    )
    rows_per_page = page_size_column.selectbox(
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
    page_count = max(1, math.ceil(total_rows / rows_per_page))

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
    visible_tracks = sorted_tracks.iloc[start : start + rows_per_page]

    st.caption(
        f"Showing {len(visible_tracks):,} of {total_rows:,} matching tracks"
    )

    if visible_tracks.empty:
        st.info("No tracks match your current search and filters.")
    else:
        st.dataframe(
            visible_tracks[selected_columns],
            width="stretch",
            hide_index=True,
        )

    return filtered
