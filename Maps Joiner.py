import folium
import pandas as pd

# Read the data
df = pd.read_excel('C:\\Users\\Lucas\\PycharmProjects\\LND\\Living New Deal.xlsx', skiprows=0)

# Load region map from HTML file
with open("C:\\Users\\Lucas\\PycharmProjects\\LND\\my_map.html", 'r') as file:
    regions_map = file.read()

# Convert "completion_year" column to numeric data type
df["completion_year"] = pd.to_numeric(df["completion_year"], errors="coerce")

# Create a string to store marker HTML elements
marker_html = ""

# Create markers for each completion year in the DataFrame
for index, row in df.iterrows():
    completion_year = row['completion_year']
    if pd.notnull(completion_year):
        # Add marker HTML element
        marker_html += f"""
        L.marker([{row["Lat"]}, {row["Lng"]}]).addTo(map)
            .bindPopup("Completion Year: {completion_year}")
            .openPopup();"""

# Inject the marker HTML into the regions_map content
regions_map = regions_map.replace("<!-- INSERT_MARKER_HERE -->", marker_html)

# Save the modified regions_map as a new HTML file
with open("C:\\Users\\Lucas\\PycharmProjects\\LND\\regions_map_with_markers.html", 'w') as file:
    file.write(regions_map)





