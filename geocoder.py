import pandas as pd
from opencage.geocoder import OpenCageGeocode

# Load your CSV file
df = pd.read_csv('addresses.csv')

# Initialize OpenCage geocoder with your API key
key = '781b89ffc5eb47ab8e1b849822beacf1'
geocoder = OpenCageGeocode(key)

# Function to get latitude and longitude
def get_lat_long(address):
    result = geocoder.geocode(address)
    if result:
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    return None, None

# Apply the function to your DataFrame
df['Latitude'], df['Longitude'] = zip(*df['address'].apply(get_lat_long))

# Save the updated DataFrame to a new CSV
df.to_csv('updated_addresses.csv', index=False)

import folium
import pandas as pd

# Load the updated CSV file
df = pd.read_csv('updated_addresses.csv')

# Create a map centered around an average location
map_osm = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

# Add markers to the map
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Code: {row['code']}"
    ).add_to(map_osm)

# Save the map as an HTML file
map_osm.save('index.html')

import folium
import pandas as pd

# Load the updated CSV file
df = pd.read_csv('updated_addresses.csv')

# Create a map centered around an average location
map_osm = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)

# Add markers to the map
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Code: {row['code']}"
    ).add_to(map_osm)

# Save the map as an HTML file
map_osm.save('index.html')

# Read the generated map.html file
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# JavaScript code to dynamically track user location and ask for permission
js_code = """
<script>
    document.addEventListener("DOMContentLoaded", function() {
        var map = L.map('map').setView([%f, %f], 12);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
        }).addTo(map);

        function updateUserLocation(position) {
            var latlng = [position.coords.latitude, position.coords.longitude];

            if (typeof userMarker !== 'undefined') {
                map.removeLayer(userMarker);
            }

            userMarker = L.marker(latlng).addTo(map)
                .bindPopup("Your current location").openPopup();

            map.setView(latlng, 16);
        }

        function onLocationError(e) {
            alert("Error accessing your location: " + e.message);
        }

        function requestLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.watchPosition(updateUserLocation, onLocationError, {
                    enableHighAccuracy: true,
                    maximumAge: 0
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }

        requestLocation();
    });
</script>
""" % (df['Latitude'].mean(), df['Longitude'].mean())  # Insert latitude and longitude here


# Insert the JavaScript code before the closing </body> tag
updated_html_content = html_content.replace("</body>", js_code + "</body>")

# Save the updated HTML content to a new file
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(updated_html_content)
