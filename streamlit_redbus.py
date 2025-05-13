import streamlit as st
import pandas as pd

# Load the CSV
csv_file = r"C:\Users\surya\Downloads\redbusdata.csv"
df = pd.read_csv(csv_file)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Rename columns for consistent reference
df.rename(columns={
    "bustype": "bus_type",
    "star_rating": "star_rating",
    "seats_available": "seat_availability"
}, inplace=True)

# Convert numeric values from strings
for col in ['duration', 'price', 'star_rating', 'seat_availability']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing route_name
df = df.dropna(subset=['route_name'])

# Function to fetch unique route names
def fetch_route_names():
    return df['route_name'].dropna().unique()

# Function to get distinct values for a route
def fetch_distinct_values(route_name, column_name):
    return df[df['route_name'] == route_name][column_name].dropna().unique()

# Filter data based on user input
def fetch_filtered_data(route_name, min_duration=None, max_duration=None, min_price=None, max_price=None,
                        bus_type=None, min_star_rating=None, max_star_rating=None,
                        min_seat_availability=None, max_seat_availability=None):
    filtered = df[df['route_name'] == route_name]

    if min_duration is not None and max_duration is not None:
        filtered = filtered[(filtered['duration'] >= min_duration) & (filtered['duration'] <= max_duration)]

    if min_price is not None and max_price is not None:
        filtered = filtered[(filtered['price'] >= min_price) & (filtered['price'] <= max_price)]

    if bus_type:
        filtered = filtered[filtered['bus_type'] == bus_type]

    if min_star_rating is not None and max_star_rating is not None:
        filtered = filtered[(filtered['star_rating'] >= min_star_rating) & (filtered['star_rating'] <= max_star_rating)]

    if min_seat_availability is not None and max_seat_availability is not None:
        filtered = filtered[(filtered['seat_availability'] >= min_seat_availability) & (filtered['seat_availability'] <= max_seat_availability)]

    return filtered

# Sidebar filters
def display_sidebar_filters(route_name):
    durations = fetch_distinct_values(route_name, "duration")
    bus_types = fetch_distinct_values(route_name, "bus_type")

    selected_bus_type = st.sidebar.selectbox("🚌 Bus Type", [None] + sorted(bus_types.tolist()))
    min_duration = st.sidebar.selectbox("⏱️ Min Duration", [None] + sorted(durations.tolist()))
    max_duration = st.sidebar.selectbox("⏱️ Max Duration", [None] + sorted(durations.tolist()))

    min_price = st.sidebar.number_input("💰 Min Price", min_value=0, step=1)
    max_price = st.sidebar.number_input("💰 Max Price", min_value=0, step=1)

    min_star_rating = st.sidebar.slider("⭐ Min Star Rating", 0, 5, 0)
    max_star_rating = st.sidebar.slider("⭐ Max Star Rating", min_star_rating, 5, 5)

    min_seat_availability = st.sidebar.slider("💺 Min Seat Availability (%)", 0, 100, 0)
    max_seat_availability = st.sidebar.slider("💺 Max Seat Availability (%)", min_seat_availability, 100, 100)

    return {
        "bus_type": selected_bus_type,
        "min_duration": min_duration,
        "max_duration": max_duration,
        "min_price": min_price if min_price > 0 else None,
        "max_price": max_price if max_price > 0 else None,
        "min_star_rating": min_star_rating,
        "max_star_rating": max_star_rating,
        "min_seat_availability": min_seat_availability,
        "max_seat_availability": max_seat_availability
    }

# Main Streamlit app
def main():
    st.title("🚌 Red Bus Route Data Viewer")

    route_names = fetch_route_names()
    selected_route = st.sidebar.selectbox("📍 Select Route Name", [None] + sorted(route_names.tolist()))

    if selected_route:
        filters = display_sidebar_filters(selected_route)
        filtered_data = fetch_filtered_data(selected_route, **filters)

        st.subheader(f"Filtered Results for: {selected_route}")
        st.dataframe(filtered_data)
    else:
        st.info("Please select a route from the sidebar to view data.")

if __name__ == "__main__":
    main()
