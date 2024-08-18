import folium
import json
from shapely.geometry import shape, LineString
from shapely.ops import unary_union
import numpy as np


# Load GeoJSON data for each state from the file
with open('C:\\Users\\Lucas\\Downloads\\states.json', 'r') as f:
    states_geojson = json.load(f)

# Define regions and the corresponding state names along with colors
regions = {
    'Region 1': (['Maine', 'New Hampshire', 'Rhode Island', 'Massachusetts', 'Vermont', 'Connecticut'], 'blue'),
    'Region 2': (['New York'], 'red'),
    'Region 3': (['New Jersey', 'Pennsylvania'], 'green'),  # Eastern half of Pennsylvania
    'Region 4': (['Virginia', 'Maryland', 'Delaware', 'District of Columbia'], 'orange'),
    'Region 5': (['Tennessee', 'North Carolina', 'South Carolina', 'Georgia', 'Florida'], 'yellow'),
    'Region 6': (['Alabama', 'Mississippi', 'Arkansas', 'Louisiana'], 'purple'),
    'Region 7': (['Missouri', 'Iowa', 'Kansas', 'Nebraska'], 'cyan'),
    'Region 8': (['Pennsylvania', 'West Virginia'], 'magenta'),  # Western half of Pennsylvania
    'Region 9': (['Michigan', 'Kentucky', 'Indiana', 'Ohio'], 'lime'),
    'Region 10': (['Wisconsin', 'Illinois', 'Minnesota'], 'pink'),
    'Region 11': (['Colorado', 'South Dakota', 'North Dakota', 'Wyoming'], 'darkblue'),
    'Region 12': (['Texas', 'Oklahoma'], 'darkred'),
    'Region 13': (['Arizona', 'New Mexico'], 'darkgreen'),
    'Region 14': (['California'], 'lightgray'),  # Southern half separated at the 35th parallel
    'Region 15': (['California', 'Nevada', 'Utah'], 'lightblue'),  # Remainder of California
    'Region 16': (['Oregon', 'Washington', 'Idaho', 'Montana'], 'lightgreen')
}

# Create a dictionary to store GeoJSON data for each region
regions_geojson = {}

# Iterate over regions and extract GeoJSON data for each region
for region, (state_names, color) in regions.items():
    region_polygons = []
    for state_geojson in states_geojson['features']:
        state_name = state_geojson['properties']['NAME']
        if state_name in state_names:
            state_geometry = shape(state_geojson['geometry'])
            if state_geometry.is_valid:
                region_polygons.append(state_geometry)
            else:
                print(f"Invalid geometry for {state_name}")
    # Create a single polygon for the region
    if region_polygons:
        region_combined_polygon = region_polygons[0] if len(region_polygons) == 1 else unary_union(region_polygons)
        if region_combined_polygon.is_valid:
            region_feature = {
                'type': 'Feature',
                'properties': {},
                'geometry': region_combined_polygon.__geo_interface__
            }
            region_geojson = {
                'type': 'FeatureCollection',
                'features': [region_feature]
            }
            regions_geojson[region] = region_geojson
        else:
            print(f"Invalid combined polygon for {region}")

# Find Pennsylvania GeoJSON data
pennsylvania_geojson = None
for state_geojson in states_geojson['features']:
    state_name = state_geojson['properties']['NAME']
    if state_name == 'Pennsylvania':
        pennsylvania_geojson = state_geojson
        break

# Extract Pennsylvania boundary coordinates
pennsylvania_coords = pennsylvania_geojson['geometry']['coordinates'][0]

# Find the bounding box of Pennsylvania
min_lon, min_lat = np.min(pennsylvania_coords, axis=0)
max_lon, max_lat = np.max(pennsylvania_coords, axis=0)
center_lat = (min_lat + max_lat) / 2  # Center latitude

# Define line coordinates along the center of the bounding box
pa_line_coords = [(center_lat, min_lon), (center_lat, max_lon)]

# Create the LineString geometry for the line down the middle of Pennsylvania
pa_line = LineString(pa_line_coords)

# Create a map centered around the United States
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

# Add GeoJSON polygons for each region
for region, region_geojson in regions_geojson.items():
    style_function = lambda feature, fill_color=regions[region][1]: {
        'fillColor': fill_color,
        'color': 'black',  # Border color
        'weight': 1,  # Border width
        'fillOpacity': 0.5,  # Opacity of the fill
    }
    folium.GeoJson(
        region_geojson,
        name=region,
        style_function=style_function
    ).add_to(m)

# Add the LineString for Pennsylvania to the map
folium.GeoJson(
    pa_line.__geo_interface__,
    name='Pennsylvania_Line',
    style_function=lambda feature: {
        'color': 'black',
        'weight': 3,  # Increase the weight to thicken the line
    }
).add_to(m)

m.save("C:\\Users\\Lucas\\PycharmProjects\\LND\\my_map.html")