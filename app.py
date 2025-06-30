import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime, date
from typing import List
from dataclasses import dataclass
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict


@dataclass
class Species:
    name: str
    category: str


@dataclass
class Sighting:
    species: Species
    surveyors: str
    date: date
    field_section: str
    count: int


# Your cleaned species list (make sure this matches what's in your Excel file)
SPECIES_LIST: List[Species] = [
    Species("Barn Owl", "Green"),
    Species("Black-headed Gull", "Amber"),
    Species("Blackbird", "Green"),
    Species("Blackcap", "Green"),
    Species("Blue Tit", "Green"),
    Species("Bullfinch", "Amber"),
    Species("Mallard", "Amber"),
    Species("Domestic Mallard", "Green"),
    Species("Buzzard", "Green"),
    Species("Canada Goose", "Green"),
    Species("Carrion Crow", "Green"),
    Species("Cattle Egret", "Amber"),
    Species("Chaffinch", "Green"),
    Species("Chiffchaff", "Green"),
    Species("Coal Tit", "Green"),
    Species("Collared Dove", "Green"),
    Species("Common Crossbill", "Green"),
    Species("Common Gull", "Amber"),
    Species("Coot", "Green"),
    Species("Cormorant", "Green"),
    Species("Cuckoo", "Red"),
    Species("Curlew", "Red"),
    Species("Dunnock", "Amber"),
    Species("Feral Pigeon", "Green"),
    Species("Fieldfare", "Red"),
    Species("Goldcrest", "Green"),
    Species("Goldfinch", "Green"),
    Species("Goshawk", "Green"),
    Species("Great Black-backed Gull", "Amber"),
    Species("Great Spotted Woodpecker", "Green"),
    Species("Great Tit", "Amber"),
    Species("Great White Egret", "Green"),
    Species("Green Sandpiper", "Green"),
    Species("Green Woodpecker", "Green"),
    Species("Greenfinch", "Red"),
    Species("Grey Heron", "Green"),
    Species("Grey Partridge", "Red"),
    Species("Grey Wagtail", "Amber"),
    Species("Greylag Goose", "Green"),
    Species("Hawfinch", "Red"),
    Species("Herring Gull", "Red"),
    Species("Hobby", "Green"),
    Species("House Martin", "Red"),
    Species("House Sparrow", "Red"),
    Species("Jack Snipe", "Green"),
    Species("Jackdaw", "Green"),
    Species("Jay", "Green"),
    Species("Kestrel", "Amber"),
    Species("Kingfisher", "Green"),
    Species("Lapwing", "Red"),
    Species("Lesser Black-backed Gull", "Amber"),
    Species("Lesser Redpoll", "Red"),
    Species("Lesser Whitethroat", "Green"),
    Species("Linnet", "Red"),
    Species("Little Egret", "Green"),
    Species("Little Owl", "Green"),
    Species("Long-tailed Tit", "Green"),
    Species("Magpie", "Green"),
    Species("Mallard duck", "Green"),
    Species("Mandarin duck", "Green"),
    Species("Marsh Tit", "Red"),
    Species("Meadow Pipit", "Amber"),
    Species("Mistle Thrush", "Red"),
    Species("Moorhen", "Amber"),
    Species("Mute Swan", "Green"),
    Species("Nightingale", "Red"),
    Species("Nuthatch", "Green"),
    Species("Partridge,red leg", "Green"),
    Species("Pheasant", "Green"),
    Species("Pied/White Wagtail", "Green"),
    Species("Quail", "Amber"),
    Species("Raven", "Green"),
    Species("Red Kite", "Green"),
    Species("Redstart", "Amber"),
    Species("Redwing", "Red"),
    Species("Reed Bunting", "Amber"),
    Species("Reed Warbler", "Green"),
    Species("Robin", "Green"),
    Species("Rook", "Amber"),
    Species("Sedge Warbler", "Amber"),
    Species("Short-eared Owl", "Amber"),
    Species("Siskin", "Green"),
    Species("Skylark", "Red"),
    Species("Snipe", "Amber"),
    Species("Song Thrush", "Red"),
    Species("Sparrowhawk", "Green"),
    Species("Spotted Flycatcher", "Red"),
    Species("Starling", "Red"),
    Species("Stock Dove", "Amber"),
    Species("Stonechat", "Green"),
    Species("Swallow", "Green"),
    Species("Swift", "Red"),
    Species("Tawny Owl", "Amber"),
    Species("Tree Pipit", "Red"),
    Species("Treecreeper", "Green"),
    Species("Turtle Dove", "Red"),
    Species("Wheatear", "Amber"),
    Species("Whinchat", "Red"),
    Species("Whitethroat", "Amber"),
    Species("Willow warbler", "Amber"),
    Species("Woodpigeon", "Amber"),
    Species("Wren", "Amber"),
    Species("Yellowhammer", "Red"),
]


def parse_excel_date(date_value):
    """Parse various date formats from Excel."""
    if pd.isna(date_value):
        return None

    try:
        if isinstance(date_value, str):
            # Handle string dates like "8.30am 3/5/2025", "9am 24/5/2025", or "8am 21/06/25"
            if "/" in date_value:
                # Extract date part from strings like "8.30am 3/5/2025" or "8am 21/06/25"
                parts = date_value.split()
                date_part = parts[-1]  # Get last part which should be the date

                # Try different date formats
                date_formats = [
                    "%d/%m/%Y",  # 21/06/2025
                    "%d/%m/%y",  # 21/06/25
                    "%m/%d/%Y",  # 06/21/2025 (US format)
                    "%m/%d/%y",  # 06/21/25 (US format)
                ]

                for date_format in date_formats:
                    try:
                        parsed_date = datetime.strptime(date_part, date_format).date()
                        # If using 2-digit year format, ensure it's interpreted correctly
                        if date_format.endswith("/%y"):
                            # Assuming years 00-30 are 2000-2030, 31-99 are 1931-1999
                            if parsed_date.year < 1950:  # Adjust this threshold as needed
                                parsed_date = parsed_date.replace(year=parsed_date.year + 100)
                        return parsed_date
                    except ValueError:
                        continue

                # If no format worked, raise an error
                raise ValueError(f"Could not parse date part '{date_part}' with any known format")

            elif "T" in date_value:
                # ISO format
                return datetime.fromisoformat(date_value.replace('Z', '+00:00')).date()
        elif isinstance(date_value, (int, float)):
            # Excel serial date - convert from Excel's 1900 epoch
            excel_epoch = datetime(1900, 1, 1)
            delta_days = int(date_value) - 2  # -2 for Excel's leap year bug (1900 wasn't a leap year)
            return (excel_epoch + pd.Timedelta(days=delta_days)).date()
        elif hasattr(date_value, 'date'):
            return date_value.date()
        else:
            return date_value
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Could not parse date '{date_value}': {e}")
        return None


def load_bird_sightings() -> List[Sighting]:
    """
    Load bird sightings from src/sightings_2024_2025.xlsx

    Returns:
        List of Sighting objects
    """
    # Updated file path to look in the src directory
    file_path = Path("sightings_2024_2025.xlsx")

    # Alternative approach using __file__ to be more robust
    # current_dir = Path(__file__).parent
    # file_path = current_dir / "sightings_2024_2025.xlsx"

    sightings = []  # Initialize the sightings list

    try:
        # Read both sheets from the Excel file
        excel_data = pd.read_excel(file_path, sheet_name=None, header=None)

        for year, sheet_name in [("2024", "Heal Somerset bird list 2024"), ("2025", "Heal Somerset bird list 2025")]:
            if sheet_name not in excel_data:
                print(f"Warning: Sheet '{sheet_name}' not found in Excel file")
                continue

            df = excel_data[sheet_name]

            # Extract header information from the first few rows
            dates_row = df.iloc[2] if len(df) > 2 else pd.Series()
            surveyors_row = df.iloc[1] if len(df) > 1 else pd.Series()
            field_sections_row = df.iloc[3] if len(df) > 3 else pd.Series()

            # Find columns that contain actual count data (skip summary columns)
            data_columns = []
            for col_idx in range(3, len(dates_row)):  # Start from column 3
                date_val = dates_row.iloc[col_idx] if col_idx < len(dates_row) else None

                if (not pd.isna(date_val) and
                        str(date_val) not in ['Monthly Totals', 'Total for 2024', 'Species Total 2024'] and
                        not str(date_val).startswith('North') and
                        not str(date_val).startswith('South') and
                        not str(date_val).startswith('East') and
                        '#DIV' not in str(date_val)):
                    data_columns.append(col_idx)

            # Process each bird species (starting from row 6)
            for row_idx in range(6, len(df)):
                if row_idx >= len(df):
                    break

                species_name = df.iloc[row_idx, 0] if not df.iloc[row_idx, 0:1].empty else None

                # Skip empty rows or rows that don't contain species names
                if pd.isna(species_name) or species_name == "":
                    continue

                # Find the Species object for this bird
                species_obj = None
                for species in SPECIES_LIST:
                    if species.name == species_name:
                        species_obj = species
                        break

                if not species_obj:
                    print(f"Warning: Species '{species_name}' not found in SPECIES_LIST")
                    continue

                # Process each survey column for this species
                for col_idx in data_columns:
                    if col_idx >= len(df.columns):
                        continue

                    count_value = df.iloc[row_idx, col_idx]

                    # Skip empty counts
                    if pd.isna(count_value) or count_value == "" or count_value == 0:
                        continue

                    try:
                        count = int(float(count_value))  # Handle floats that should be ints
                    except (ValueError, TypeError):
                        continue

                    # Extract date
                    date_value = dates_row.iloc[col_idx] if col_idx < len(dates_row) else None
                    survey_date = parse_excel_date(date_value)

                    if not survey_date:
                        continue

                    # Extract surveyors
                    surveyors = (str(surveyors_row.iloc[col_idx])
                                 if col_idx < len(surveyors_row) and not pd.isna(surveyors_row.iloc[col_idx])
                                 else "Unknown")

                    # Extract field section
                    field_section = (str(field_sections_row.iloc[col_idx])
                                     if col_idx < len(field_sections_row) and not pd.isna(
                        field_sections_row.iloc[col_idx])
                                     else "Unknown")

                    # Create sighting object
                    sighting = Sighting(
                        species=species_obj,
                        surveyors=surveyors,
                        date=survey_date,
                        field_section=field_section,
                        count=count
                    )

                    sightings.append(sighting)

    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return []

    return sightings


def get_bird_sightings() -> List[Sighting]:
    return load_bird_sightings()


def filter_sightings(sightings: List[Sighting], conservation_statuses=None, years=None, locations=None):
    """Filter sightings based on selected criteria."""
    filtered = sightings

    if conservation_statuses and len(conservation_statuses) < 3:  # Only filter if not all are selected
        filtered = [s for s in filtered if s.species.category in conservation_statuses]

    if years:
        filtered = [s for s in filtered if s.date.year in years]

    if locations:
        filtered = [s for s in filtered if s.field_section in locations]

    return filtered


def create_species_chart(sightings: List[Sighting]):
    """Create a bar chart of species sightings colored by conservation status."""
    # Calculate species counts
    species_data = defaultdict(lambda: {'count': 0, 'category': ''})

    for sighting in sightings:
        species_data[sighting.species.name]['count'] += sighting.count
        species_data[sighting.species.name]['category'] = sighting.species.category

    # Convert to list and sort by count (descending)
    species_list = [(name, data['count'], data['category'])
                    for name, data in species_data.items()]
    species_list.sort(key=lambda x: x[1], reverse=True)

    # Prepare data for plotting
    species_names = [item[0] for item in species_list]
    counts = [item[1] for item in species_list]
    categories = [item[2] for item in species_list]

    # Color mapping for conservation status
    color_map = {'Green': '#2E7D32', 'Amber': '#F57C00', 'Red': '#C62828'}
    colors = [color_map[cat] for cat in categories]

    # Create plotly bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=species_names,
            y=counts,
            marker_color=colors,
        )
    ])

    fig.update_layout(
        title="Species Sightings by Conservation Status",
        xaxis_title="Species",
        yaxis_title="Total Count",
        xaxis={'tickangle': 45},
        height=600,
        showlegend=False
    )

    return fig


def create_monthly_timeline(sightings: List[Sighting], selected_species: List[str]):
    """Create a monthly timeline chart for selected species."""
    if not selected_species:
        return None

    # Filter sightings for selected species
    filtered_sightings = [s for s in sightings if s.species.name in selected_species]

    # Group by species and month
    monthly_data = defaultdict(lambda: defaultdict(int))

    for sighting in filtered_sightings:
        month_key = f"{sighting.date.year}-{sighting.date.month:02d}"
        monthly_data[sighting.species.name][month_key] += sighting.count

    # Create DataFrame for plotting
    plot_data = []
    for species_name, months in monthly_data.items():
        for month_key, count in months.items():
            plot_data.append({
                'Species': species_name,
                'Month': month_key,
                'Count': count
            })

    df = pd.DataFrame(plot_data)

    if df.empty:
        return None

    # Create bar chart
    fig = px.bar(df, x='Month', y='Count', color='Species',
                 title=f"Monthly Sightings Timeline",
                 labels={'Count': 'Total Birds Counted'})

    fig.update_layout(height=400, xaxis={'tickangle': 45})

    return fig


def main():
    st.set_page_config(
        page_title="Heal Somerset Bird Survey",
        page_icon="🦅",
        layout="wide"
    )

    st.title("🦅 Heal Somerset Bird Survey Dashboard")
    st.markdown("Welcome to the bird sightings analysis dashboard for Heal Somerset.")

    # Load the sightings data
    with st.spinner("Loading bird sightings data..."):
        try:
            sightings = get_bird_sightings()

            if sightings:
                # Get unique values for filters
                all_years = sorted(list(set(s.date.year for s in sightings)))
                all_locations = sorted(list(set(s.field_section for s in sightings)))
                all_conservation_statuses = ["Green", "Amber", "Red"]

                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Species Detail", "📋 Raw Data"])

                with tab1:
                    st.header("Survey Overview")

                    # Filters
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        selected_conservation = st.multiselect("Conservation Status:", all_conservation_statuses,
                                                               default=all_conservation_statuses)
                    with col2:
                        selected_years = st.multiselect("Years:", all_years, default=all_years)
                    with col3:
                        selected_locations = st.multiselect("Locations:", all_locations, default=all_locations)

                    # Apply filters
                    filtered_sightings = filter_sightings(
                        sightings,
                        selected_conservation,
                        selected_years,
                        selected_locations
                    )

                    # Display species count
                    unique_species = len(set(s.species.name for s in filtered_sightings))
                    st.metric("Species Observed", f"{unique_species} species")

                    # Species chart
                    if filtered_sightings:
                        fig = create_species_chart(filtered_sightings)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No data available for the selected filters.")

                with tab2:
                    st.header("Species Details & Timeline")

                    # Species selector (multi-select)
                    all_species = sorted(list(set(s.species.name for s in sightings)))
                    selected_species = st.multiselect("Select species:", all_species,
                                                      default=[all_species[0]] if all_species else [])

                    if selected_species:
                        # Create summary table for selected species
                        species_summary_data = []
                        for species_name in selected_species:
                            species_sightings = [s for s in sightings if s.species.name == species_name]
                            species_obj = species_sightings[0].species if species_sightings else None

                            if species_obj:
                                species_summary_data.append({
                                    "Species": species_name,
                                    "Conservation Status": species_obj.category,
                                    "Total Sightings": sum(s.count for s in species_sightings)
                                })

                        # Display summary table
                        if species_summary_data:
                            summary_df = pd.DataFrame(species_summary_data)
                            st.dataframe(summary_df, use_container_width=True, hide_index=True)

                        # Monthly timeline chart
                        timeline_fig = create_monthly_timeline(sightings, selected_species)
                        if timeline_fig:
                            st.plotly_chart(timeline_fig, use_container_width=True)
                        else:
                            st.info("No sightings data available for the selected species.")

                with tab3:
                    st.header("Raw Sightings Data")

                    # Convert to DataFrame for display
                    df_data = []
                    for sighting in sightings:
                        df_data.append({
                            "Date": sighting.date,
                            "Species": sighting.species.name,
                            "Conservation Status": sighting.species.category,
                            "Count": sighting.count,
                            "Location": sighting.field_section,
                            "Surveyors": sighting.surveyors
                        })

                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True)

                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name="heal_somerset_bird_sightings.csv",
                        mime="text/csv"
                    )

            else:
                st.error("❌ No sightings could be loaded from the file.")
                st.info("Please check that the file exists at: `/data/sightings_2024_2025.xlsx`")

        except FileNotFoundError:
            st.error("❌ File not found: `/data/sightings_2024_2025.xlsx`")
            st.info("Please ensure the Excel file is in the correct location.")
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.info("Please check the file format and try again.")


if __name__ == "__main__":
    main()