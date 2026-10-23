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
    search_text = st.sidebar.text_input(
        "Search tracks, artists, albums, or genres"
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
            searchable_text.str.contains(search_text, case=False, regex=False)
        ]

    if "track_genre" in filtered.columns:
        genres = sorted(filtered["track_genre"].dropna().astype(str).unique())
        selected_genres = st.sidebar.multiselect(
            "Genres",
            genres,
            default=genres,
        )
        filtered = filtered[filtered["track_genre"].isin(selected_genres)]

    if "popularity" in filtered.columns:
        popularity = pd.to_numeric(filtered["popularity"], errors="coerce")
        if popularity.notna().any():
            low = int(popularity.min())
            high = int(popularity.max())
            if low < high:
                selected_range = st.sidebar.slider(
                    "Popularity range",
                    min_value=low,
                    max_value=high,
                    value=(low, high),
                )
                filtered = filtered[
                    filtered["popularity"].between(*selected_range)
                ]

    if "explicit" in filtered.columns:
        explicit_filter = st.sidebar.selectbox(
            "Explicit content",
            ["All tracks", "Explicit only", "Non-explicit only"],
        )
        if explicit_filter == "Explicit only":
            filtered = filtered[filtered["explicit"] == True]
        elif explicit_filter == "Non-explicit only":
            filtered = filtered[filtered["explicit"] == False]

    st.subheader("Explore tracks")
    available_columns = [column for column in DEFAULT_COLUMNS if column in filtered.columns]
    if not available_columns:
        st.info("No recognized track columns are available to display.")
        return filtered

    selected_columns = st.multiselect(
        "Columns",
        available_columns,
        default=available_columns,
    )
    if not selected_columns:
        st.info("Choose at least one column to display the track table.")
        return filtered

    sort_column, sort_order, page_size = st.columns([2, 1, 1])
    sort_by = sort_column.selectbox("Sort by", selected_columns)
    descending = sort_order.checkbox("Descending", value=True)
    rows_per_page = page_size.selectbox("Rows per page", [25, 50, 100, 250])

    sorted_tracks = filtered.sort_values(
        by=sort_by,
        ascending=not descending,
        na_position="last",
    )
    page_count = max(1, (len(sorted_tracks) + rows_per_page - 1) // rows_per_page)
    page = st.number_input(
        "Page",
        min_value=1,
        max_value=page_count,
        value=1,
        step=1,
    )
    start = (page - 1) * rows_per_page
    visible_tracks = sorted_tracks.iloc[start : start + rows_per_page]

    st.caption(f"Showing {len(visible_tracks):,} of {len(filtered):,} matching tracks")
    st.dataframe(
        visible_tracks[selected_columns],
        use_container_width=True,
        hide_index=True,
    )
    return filtered