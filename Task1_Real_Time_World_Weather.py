import requests
import folium
import json
import webbrowser
from flask import Flask, render_template_string, request

# Replace with your actual OpenWeatherMap API key
API_KEY = "40ac47e4005574438c138af06e000fdb"

app = Flask(__name__)

# HTML Template for the interactive world map
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Weather Dashboard</title>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <style>
        #map { height: 100vh; }
        .info-box {
            position: absolute;
            top: 10px;
            right: 10px;
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.3);
            font-size: 14px;
            min-width: 220px;
            text-align: left;
            z-index: 1000;
            font-family: Arial, sans-serif;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([20, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        var infoBox = L.control({position: 'topright'});
        infoBox.onAdd = function(map) {
            this._div = L.DomUtil.create('div', 'info-box');
            this.update();
            return this._div;
        };
        infoBox.update = function(content) {
            this._div.innerHTML = content || 'Hover over a location';
        };
        infoBox.addTo(map);

        function fetchWeather(lat, lon) {
            fetch(`/get_weather?lat=${lat}&lon=${lon}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    infoBox.update(`Error: ${data.error}`);
                } else {
                    infoBox.update(`
                        <b>${data.city}, ${data.country}</b><br>
                        Lat: ${lat}, Lon: ${lon}<br>
                        Temp: ${data.temp}°C<br>
                        Humidity: ${data.humidity}%<br>
                        ${data.description}
                    `);
                }
            })
            .catch(error => {
                console.error("Fetch error:", error);
                infoBox.update("Failed to fetch weather data.");
            });
        }

        map.on('mousemove', function(e) {
            var lat = e.latlng.lat.toFixed(4);
            var lon = e.latlng.lng.toFixed(4);
            infoBox.update(`Lat: ${lat}, Lon: ${lon}<br>Fetching weather...`);
            fetchWeather(lat, lon);
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_weather')
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    try:
        geo_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url).json()
        if not geo_response:
            return json.dumps({"error": "City not found"})
        city = geo_response[0]['name']
        country = geo_response[0]['country']

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather_response = requests.get(weather_url).json()

        if "main" not in weather_response:
            return json.dumps({"error": "Weather data unavailable"})
        
        return json.dumps({
            "city": city,
            "country": country,
            "temp": weather_response['main']['temp'],
            "humidity": weather_response['main']['humidity'],
            "description": weather_response['weather'][0]['description'].capitalize()
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
