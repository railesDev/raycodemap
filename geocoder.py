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
df.to_csv('updated_file.csv', index=False)
import folium

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

# Read the existing map.html file
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# JavaScript code to dynamically track user location
js_code = """
<script>
    // Initialize the map
    var map = L.map('map').setView([{{ df['Latitude'].mean() }}, {{ df['Longitude'].mean() }}], 12);

    // Add OSM tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
    }).addTo(map);

    // Function to update user location on the map
    function updateUserLocation(position) {
        var latlng = [position.coords.latitude, position.coords.longitude];

        // Remove previous marker if exists
        if (typeof userMarker !== 'undefined') {
            map.removeLayer(userMarker);
        }

        // Add new marker for user's current location
        userMarker = L.marker(latlng).addTo(map)
            .bindPopup("Your current location").openPopup();

        // Update map view to user's current location
        map.setView(latlng, 16);
    }

    // Function to handle errors in getting user location
    function onLocationError(e) {
        alert("Error accessing your location: " + e.message);
    }

    // Function to request permission for geolocation
    function requestLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(updateUserLocation, onLocationError, {
                enableHighAccuracy: true,
                maximumAge: 0
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    // Ask for permission when the page loads
    requestLocation();
</script>
"""


# Insert the JavaScript code before the closing </body> tag
updated_html_content = html_content.replace("</body>", js_code + "</body>")

# Save the updated HTML content to a new file
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(updated_html_content)

