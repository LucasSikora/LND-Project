import pandas as pd
import folium

# Read the data
df = pd.read_excel('C:\\Users\\Lucas\\PycharmProjects\\LND\\Living New Deal.xlsx', skiprows=0)

# Convert "completion_year" column to numeric data type
df["completion_year"] = pd.to_numeric(df["completion_year"], errors="coerce")

# Create a Folium map centered around the mean of all coordinates
map_center = [df["Lat"].mean(), df["Lng"].mean()]
mymap = folium.Map(location=map_center, zoom_start=5)

# Create markers for each completion year in the DataFrame
for index, row in df.iterrows():
    completion_year = row['completion_year']
    if pd.notnull(completion_year):
        folium.Marker(
            location=[row["Lat"], row["Lng"]],
            popup=f"Completion Year: {completion_year}",
            icon=folium.Icon(color='green'),  # Green marker for completion year
            tooltip=f"Completion Year: {completion_year}",
            data_completion_year=completion_year
        ).add_to(mymap)

# Open and read the content of my_map.html
with open('C:\\Users\\Lucas\\PycharmProjects\\LND\\my_map.html', 'r') as f:
    map2_content = f.read()

# Adjust the styles to position the elements from my_map.html on top of the Folium map
map2_content_with_styles = """
<div style="position: absolute; top: 0; left: 0; z-index: 1000; background-color: transparent;">
""" + map2_content + """
</div>
"""

# Append the adjusted content of my_map.html to mymap
mymap.get_root().html.add_child(folium.Element(map2_content_with_styles))

# Save the map as an HTML file
mymap.save("C:\\Users\\Lucas\\PycharmProjects\\LND\\coord_map.html")










