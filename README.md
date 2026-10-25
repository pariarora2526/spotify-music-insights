 
# 🎵 SoundScape — Spotify Music Insights Dashboard

**An interactive music analytics dashboard built with Python, Streamlit, Pandas, and Plotly.**

Explore music tracks, compare genres, analyze artists, understand audio characteristics, and discover patterns in Spotify track data through an interactive dashboard.

**Repository:** [spotify-music-insights](https://github.com/pariarora2526/spotify-music-insights)

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Project Objectives](#-project-objectives)
3. [Features](#-features)
4. [Technology Stack](#-technology-stack)
5. [How the Project Was Built](#-how-the-project-was-built)
6. [Data Cleaning and Preparation](#-data-cleaning-and-preparation)
7. [Dashboard Modules](#-dashboard-modules)
8. [Project Structure](#-project-structure)
9. [Installation and Setup](#-installation-and-setup)
10. [Running the Dashboard](#-running-the-dashboard)
11. [Understanding the Code](#-understanding-the-code)
12. [GitHub Collaboration Workflow](#-github-collaboration-workflow)
13. [Current Limitations](#-current-limitations)
14. [Future Improvements](#-future-improvements)
15. [Learning Outcomes](#-learning-outcomes)

---

## 🎯 Project Overview

SoundScape is a data analytics project designed to explore and understand music data through an interactive web dashboard.

Music datasets contain information about tracks, artists, albums, genres, popularity, and audio characteristics. Examining these attributes in a spreadsheet can make it difficult to identify patterns or compare different groups of tracks.

This project transforms a CSV dataset into a visual analytics interface where users can explore the collection, compare music genres, inspect audio features, search for tracks, and export selected data.

The application is built with Streamlit, allowing Python code to be converted into an interactive web application without requiring a separate frontend framework.

### Project at a glance

| Component | Details |
|---|---|
| Project name | SoundScape — Spotify Music Insights |
| Project type | Interactive data analytics dashboard |
| Programming language | Python |
| User interface | Streamlit |
| Data processing | Pandas and NumPy |
| Visualizations | Plotly |
| Data source format | CSV |
| Version control | Git and GitHub |
| Development environment | Local Python environment |

The dashboard currently works with the local dataset stored at `data/spotify_tracks.csv`. It analyzes the supplied dataset rather than fetching live Spotify streaming information.

---

## 🎯 Project Objectives

- Convert raw music data into a structured, usable dataset.
- Clean inconsistent values and handle missing or invalid data.
- Calculate useful summary statistics about tracks, artists, and genres.
- Visualize popularity distributions and audio characteristics.
- Provide interactive search, filtering, sorting, and pagination.
- Allow users to export filtered results as CSV files.
- Build a practical data analytics project using free and accessible tools.
- Practice collaborative software development using Git and GitHub.

---

## ✨ Features

### 1. Interactive dashboard interface

- Dark, Spotify-inspired visual theme.
- Responsive, wide-layout dashboard.
- Custom styling and music-inspired visual elements.
- Organized analytics tabs for easier navigation.

### 2. Dataset overview

The dashboard displays key metrics calculated from the loaded dataset, including:

- Total number of tracks.
- Number of artist entries.
- Number of distinct genres.
- Average track popularity.

It also highlights popular tracks in the collection.

### 3. Genre discovery

Explore the distribution of tracks across different genres and compare genre-level patterns using interactive visualizations.

### 4. Artist insights

Explore artist-related information and compare tracks and popularity within the dataset.

### 5. Audio feature analysis

Analyze available audio characteristics, including:

- Danceability
- Energy
- Speechiness
- Acousticness
- Instrumentalness
- Liveness
- Valence
- Tempo

These features help describe different characteristics of the music. Their interpretation depends on the definitions and scale of the original dataset.

### 6. Track explorer

The interactive track explorer supports:

- Searching track names, artists, albums, and genres.
- Filtering by genre.
- Filtering by popularity range.
- Filtering by explicit-content status.
- Selecting the columns to display.
- Sorting data by selected columns.
- Choosing the number of rows per page.
- Navigating through paginated results.
- Viewing the most popular tracks matching the selected filters.

### 7. CSV export

Users can download the filtered track selection as a CSV file for further analysis in Python, Excel, or other compatible tools.

### 8. Data quality reporting

The data preparation utilities can report dataset dimensions, duplicate rows, missing values, and missing-value percentages to help assess data quality.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Dashboard interface and interactive controls |
| Pandas | Loading, cleaning, transforming, and filtering tabular data |
| NumPy | Numerical data handling |
| Plotly Express | Interactive charts and visualizations |
| Git | Tracking changes in source code |
| GitHub | Hosting the repository and collaborating |
| VS Code / PowerShell | Development and command-line execution |

The project is designed to run locally using free tools. No paid dashboard platform or cloud hosting service is required for local development.

---

## 🏗️ How the Project Was Built

The project follows a simple data analytics workflow:

```text
Raw CSV Dataset
       |
       v
Load the Dataset
       |
       v
Clean and Validate Data
       |
       v
Prepare Structured DataFrame
       |
       v
Calculate Summary Metrics
       |
       v
Create Interactive Visualizations
       |
       v
Add Search and Filtering
       |
       v
Display Track Explorer
       |
       v
Export Filtered Results
```

### Step 1: Project planning

The project began with the idea of creating a practical music analytics dashboard that would be more interactive than a static spreadsheet.

Streamlit was selected because it allows dashboards to be built directly in Python, making it suitable for a beginner-friendly data analytics project.

### Step 2: Setting up the development environment

Python was used as the main programming language. The required libraries were installed through `pip`.

The project was organized into separate Python files so that data preparation, track exploration, and dashboard presentation could be maintained independently.

### Step 3: Collecting and storing the dataset

The application reads the music dataset from:

```text
data/spotify_tracks.csv
```

The dataset contains track metadata, popularity information, content flags, genres, and audio features.

The current prepared dataset contains approximately **113,550 rows and 20 columns**. These figures describe the current dataset and may change if the data is updated.

The CSV file acts as the input to the application.

> Dataset attribution: Include the original dataset publisher, source URL, and applicable license or usage terms here before distributing the dataset publicly. This project does not require a live Spotify API connection to run.

### Step 4: Building the data-cleaning module

A dedicated utility module was created to load and prepare the data before it reaches the dashboard.

This separation makes the application easier to maintain: cleaning logic can be improved without rewriting the visualizations.

The cleaning workflow handles column-name standardization, text cleanup, numeric conversion, invalid values, explicit-content flags, and duplicate records.

### Step 5: Building the track explorer

The track explorer was separated into its own module.

It provides search, filters, column selection, sorting, and pagination. Keeping these controls separate from the main dashboard makes the code more organized and allows the exploration functionality to be maintained independently.

### Step 6: Designing the dashboard

Streamlit was used to build the page layout, metrics, tabs, and interactive controls.

Plotly was used to create interactive charts. Custom CSS was added to create a dark, music-inspired visual identity.

The dashboard was organized into multiple tabs so that users can move between the overview, genre discovery, artist insights, audio analysis, and track explorer.

### Step 7: Adding export functionality

The track explorer returns the filtered dataset to the main application.

The dashboard converts the selected records into CSV format and provides a download control, allowing users to continue their analysis outside the application.

### Step 8: Testing and refining

The dashboard was run locally and checked for data-loading issues, filter behavior, chart rendering, and CSV export.

The data quality report provides an additional way to inspect the dataset and identify potential data problems.

### Step 9: Version control and collaboration

Git was used to track code changes, while GitHub was used to host the repository.

This allows both collaborators to retrieve the latest version, contribute changes, and maintain a shared project history.

---

## 🧹 Data Cleaning and Preparation

Raw datasets can contain missing values, inconsistent text, invalid numeric values, and duplicate records. The project uses a dedicated cleaning process to make the data more suitable for analysis.

### Cleaning operations

| Operation | Purpose |
|---|---|
| Column-name standardization | Make column names consistent and easier to reference |
| Text trimming | Remove unnecessary spaces from text values |
| Numeric conversion | Convert numerical fields into usable numeric types |
| Infinity handling | Replace infinite numeric values with missing values |
| Popularity validation | Treat values outside the expected 0–100 range as invalid |
| Audio-feature validation | Check feature values against their expected 0–1 range |
| Duration validation | Treat non-positive track durations as invalid |
| Tempo validation | Treat non-positive tempo values as invalid |
| Key and mode validation | Check values against their expected ranges |
| Explicit flag normalization | Standardize explicit-content values into a consistent boolean representation |
| Duplicate removal | Remove exact duplicate rows |
| Missing-value reporting | Report missing counts and percentages for data-quality inspection |

Invalid values are handled according to the field being processed. Missing values are not automatically equivalent to zero, and not every missing value needs to be removed from the dataset.

The cleaning process aims to preserve useful records while preventing obviously invalid values from misleading the analysis.

### Why data cleaning matters

For example, a duration stored as text cannot reliably be used in numerical calculations until it has been converted to a numeric value. Similarly, an invalid popularity score can distort summary statistics.

Cleaning the data before calculating metrics and creating charts makes the dashboard more reliable.

---

## 📊 Dashboard Modules

### 1. Overview

Provides a high-level snapshot of the music collection, including summary metrics, popular tracks, and visualizations of the dataset.

### 2. Genre Discovery

Helps users explore how tracks are distributed across genres and compare genre-level patterns.

### 3. Artist Insights

Provides an artist-focused view of the collection, supporting exploration of artist entries and track popularity.

### 4. Audio Features

Visualizes selected audio characteristics, including feature-score comparisons and tempo distribution.

### 5. Track Explorer

Allows users to search, filter, sort, inspect, and export track records.

These modules are intended to work together: the overview provides context, the analytics tabs support investigation, and the track explorer provides access to individual records.

---

## 📁 Project Structure

The main project files are organized as follows:

```text
spotify-music-insights/
│
├── app.py
│
├── data_utils.py
│
├── table_view.py
│
├── check_data.py
│
├── data/
│   └── spotify_tracks.csv
│
├── .streamlit/
│   └── config.toml
│
├── README.md
│
└── .gitignore
```

The structure above lists the main files used by the project. Other local files, such as a virtual environment, may exist but do not need to be committed to GitHub.

### File descriptions

| File or folder | Responsibility |
|---|---|
| `app.py` | Main Streamlit application, layout, metrics, charts, analytics tabs, and CSV export |
| `data_utils.py` | Dataset loading, cleaning, validation, and data-quality reporting |
| `table_view.py` | Track search, filtering, column selection, sorting, and pagination |
| `check_data.py` | Local script for checking dataset quality |
| `data/spotify_tracks.csv` | CSV dataset used by the dashboard |
| `.streamlit/config.toml` | Streamlit application configuration and visual settings |
| `README.md` | Project documentation |
| `.gitignore` | Specifies local or unnecessary files that Git should not track |

---

## ⚙️ Installation and Setup

Follow these steps to run the project on your computer.

### Prerequisites

Install the following:

- Python 3.10 or a compatible newer version.
- Git.
- A code editor such as Visual Studio Code.

### Step 1: Clone the repository

Open PowerShell or a terminal and run:

```bash
git clone https://github.com/pariarora2526/spotify-music-insights.git
```

Move into the project directory:

```bash
cd spotify-music-insights
```

### Step 2: Create a virtual environment

A virtual environment keeps the project's Python dependencies separate from other Python projects.

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation because of its execution policy, you can use the environment's Python executable directly instead of changing system settings.

### Step 3: Install dependencies

Run:

```powershell
python -m pip install --upgrade pip
python -m pip install streamlit pandas numpy plotly
```

These are the main libraries used by the application.

### Step 4: Check the dataset

Make sure the CSV file exists at:

```text
data/spotify_tracks.csv
```

If the dataset is missing, obtain it from the authorized source and place it at that location. The application expects the file at this path by default.

### Step 5: Run the dashboard

Execute:

```powershell
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to interact with the dashboard.

To stop the application, return to the terminal and press `Ctrl + C`.

---

## 🧩 Understanding the Code

The application separates its responsibilities into three main modules.

### `data_utils.py` — Data preparation

This module prepares the raw CSV data for analysis.

Its main responsibilities include:

1. Loading the CSV file.
2. Standardizing column names.
3. Cleaning text values.
4. Converting numeric columns.
5. Handling invalid values and exact duplicates.
6. Reporting missing values and dataset dimensions.

The main loading function is:

```python
load_tracks()
```

The main dashboard uses this function to retrieve the cleaned dataset.

### `table_view.py` — Interactive data exploration

This module contains the track explorer.

Its main function is:

```python
render_track_explorer(df)
```

It receives the prepared DataFrame and presents the search, filtering, sorting, column-selection, and pagination controls. It returns the filtered data to the main application for further display and export.

### `app.py` — Dashboard presentation

This is the application's entry point.

It is responsible for:

1. Configuring the Streamlit page.
2. Loading the dataset.
3. Caching the loaded data with Streamlit.
4. Displaying summary metrics.
5. Creating charts using Plotly.
6. Organizing analytics into tabs.
7. Calling the track explorer.
8. Displaying popular tracks from the selected results.
9. Providing the filtered CSV download.

Separating these modules makes it easier to add features without putting all the logic into a single large file.

---

## 🤝 GitHub Collaboration Workflow

This project can be developed collaboratively using Git and GitHub.

### Before starting work

Always retrieve the latest changes:

```bash
git pull origin main
```

### After making changes

Check which files have changed:

```bash
git status
```

Stage the files you want to include:

```bash
git add app.py data_utils.py table_view.py
```

If you have modified other project files, stage those as well. Review the staged changes before committing.

Create a commit:

```bash
git commit -m "Describe your changes"
```

Push the commit to GitHub:

```bash
git push origin main
```

### Collaboration guidelines

- Pull the latest changes before starting a new task.
- Make focused commits with clear messages.
- Test the dashboard before pushing.
- Avoid committing `.venv`, Python cache files, or secret credentials.
- Coordinate changes when both collaborators need to edit the same file.
- Never use force-push to overwrite another person's work.

If both collaborators edit the same section of a file, Git may report a merge conflict. Resolve it carefully before pushing.

---

## ⚠️ Current Limitations

- The dashboard analyzes the local CSV dataset and does not automatically retrieve live Spotify data.
- Results depend on the quality and completeness of the supplied dataset.
- Popularity values reflect the dataset's recorded values and should not be interpreted as live streaming counts.
- Audio-feature comparisons depend on the fields available in the dataset.
- The dashboard is currently designed as a local Streamlit application; public deployment is a separate step.
- The dataset's original source and usage license should be verified and documented before redistributing the data.

---

## 🚀 Future Improvements

Possible future enhancements include:

- Adding date or release-year analysis if suitable fields are available.
- Adding more detailed artist and genre comparisons.
- Introducing additional interactive chart controls.
- Improving accessibility and small-screen layouts.
- Adding automated data-quality tests.
- Creating a documented dependency file such as `requirements.txt`.
- Deploying the application to a suitable hosting platform.
- Adding screenshots or a short demonstration video to the repository.
- Improving the automated testing and validation workflow.

These are potential improvements rather than features claimed to be complete.

---

## 🎓 Learning Outcomes

Developing this project provides practical experience with:

- Python programming and modular code organization.
- CSV loading and data manipulation using Pandas.
- Data validation and cleaning.
- Exploratory data analysis.
- Interactive charts with Plotly.
- Building web dashboards with Streamlit.
- User-driven filtering and tabular data exploration.
- Exporting data for further analysis.
- Version control with Git.
- Collaborative development through GitHub.
- Writing technical documentation for a software project.

---

## 🏁 Conclusion

SoundScape demonstrates how a raw music dataset can be transformed into an interactive data analytics application using Python.

The project brings together data preparation, exploratory visualization, interactive filtering, and data export in one interface. Its modular structure also provides a foundation for future improvements and collaborative development.

**Built with Python, Streamlit, Pandas, NumPy, Plotly, Git, and GitHub.**

*Music, made meaningful.*
