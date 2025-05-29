import requests
import random

class WeatherFeatureExtractor:
    def __init__(self, locationiq_key, weatherapi_key):
        self.locationiq_key = locationiq_key
        self.weatherapi_key = weatherapi_key

    def derive_soil_moisture(self, rainfall_mm, temperature_c, humidity_percent):
        return min(100, max(5, rainfall_mm * 0.4 + humidity_percent * 0.3 - temperature_c * 0.5 + random.gauss(0, 5)))

    def derive_river_level(self, rainfall_mm):
        return min(6.5, max(0, rainfall_mm * 0.02 + random.gauss(0.2, 0.5)))

    def derive_vegetation_index(self, humidity_percent, rainfall_mm):
        return max(0, min(1, 0.005 * humidity_percent + 0.003 * rainfall_mm + random.gauss(0, 0.05)))

    def derive_slope_angle(self):
        return random.uniform(5, 30)

    def get_lat_lon(self, location_name):
        url = f"https://us1.locationiq.com/v1/search.php?key={self.locationiq_key}&q={location_name}&format=json"
        res = requests.get(url).json()
        if isinstance(res, list) and res:
            lat = float(res[0]["lat"])
            lon = float(res[0]["lon"])
            display_name = res[0]["display_name"]
            return lat, lon, display_name
        else:
            raise ValueError("Location not found with LocationIQ.")

    def get_weather_features(self, lat, lon):
        url = f"http://api.weatherapi.com/v1/current.json?key={self.weatherapi_key}&q={lat},{lon}"
        res = requests.get(url).json()

        temperature_c = res["current"]["temp_c"]
        humidity_percent = res["current"]["humidity"]
        wind_speed_kmph = res["current"]["wind_kph"]
        rainfall_mm = res["current"].get("precip_mm", 0.0)

        return {
            "temperature_c": temperature_c,
            "humidity_percent": humidity_percent,
            "wind_speed_kmph": wind_speed_kmph,
            "rainfall_mm": rainfall_mm,
            "soil_moisture": self.derive_soil_moisture(rainfall_mm, temperature_c, humidity_percent),
            "river_level_m": self.derive_river_level(rainfall_mm),
            "vegetation_index": self.derive_vegetation_index(humidity_percent, rainfall_mm),
            "slope_angle_deg": self.derive_slope_angle()
        }

    def extract_features_from_location(self, location_name):
        lat, lon, resolved_name = self.get_lat_lon(location_name)
        features = self.get_weather_features(lat, lon)
        return resolved_name, lat, lon, features