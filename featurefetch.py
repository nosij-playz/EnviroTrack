import requests

def safe_get(url, params=None, timeout=15):
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return {}

def first_valid(lst):
    for v in lst:
        if v is not None:
            return v
    return None

def get_env_data(lat, lon, owm_key, weatherapi_key, iqair_key):
    data = {}

    # 🌦 OpenWeatherMap: Weather features
    res = safe_get("https://api.openweathermap.org/data/2.5/weather", {
        "lat": lat, "lon": lon, "units": "metric", "appid": owm_key
    })
    if "main" in res:
        data.update({
            "temperature": res["main"].get("temp"),
            "feels_like": res["main"].get("feels_like"),
            "temp_min": res["main"].get("temp_min"),
            "temp_max": res["main"].get("temp_max"),
            "pressure": res["main"].get("pressure"),
            "humidity": res["main"].get("humidity")
        })
    data.update({
        "wind_speed": res.get("wind", {}).get("speed"),
        "wind_deg": res.get("wind", {}).get("deg"),
        "wind_gust": res.get("wind", {}).get("gust"),
        "cloud_coverage": res.get("clouds", {}).get("all"),
        "rain_1h": res.get("rain", {}).get("1h", 0),
        "rain_3h": res.get("rain", {}).get("3h", 0),
        "visibility": res.get("visibility")
    })

    # 🌤 WeatherAPI: More current features
    res = safe_get("https://api.weatherapi.com/v1/current.json", {
        "key": weatherapi_key, "q": f"{lat},{lon}", "aqi": "yes"
    })
    if "current" in res:
        current = res["current"]
        data.update({
            "uv_index": current.get("uv"),
            "visibility_km": current.get("vis_km"),
            "wind_dir": current.get("wind_dir"),
            "wind_kph": current.get("wind_kph"),
            "gust_kph": current.get("gust_kph"),
            "precip_mm": current.get("precip_mm")
        })
        if "air_quality" in current:
            aq = current["air_quality"]
            data.update({
                "co": aq.get("co"),
                "no2": aq.get("no2"),
                "o3": aq.get("o3"),
                "so2": aq.get("so2"),
                "pm2_5": aq.get("pm2_5"),
                "pm10": aq.get("pm10")
            })

    # 🌍 Open-Meteo: ECMWF Soil, Pressure, Snow, Radiation
    hourly_vars = [
        "soil_temperature_0_to_7cm", "soil_temperature_7_to_28cm",
        "soil_temperature_28_to_100cm", "soil_temperature_100_to_255cm",
        "soil_moisture_0_to_7cm", "soil_moisture_7_to_28cm",
        "soil_moisture_28_to_100cm", "soil_moisture_100_to_255cm",
        "surface_pressure", "snowfall", "snow_depth", "shortwave_radiation",
        "temperature_2m", "precipitation", "windspeed_10m", "windgusts_10m"
    ]
    res = safe_get("https://api.open-meteo.com/v1/ecmwf", {
        "latitude": lat, "longitude": lon,
        "hourly": ",".join(hourly_vars),
        "current_weather": True,
        "timezone": "auto"
    })
    if "current_weather" in res:
        data["temperature_openmeteo"] = res["current_weather"].get("temperature")
        data["windspeed_openmeteo"] = res["current_weather"].get("windspeed")

    hourly = res.get("hourly", {})
    for var in hourly_vars:
        data[var] = first_valid(hourly.get(var, []))

    # 🏭 IQAir: Air Pollution
    res = safe_get("https://api.airvisual.com/v2/nearest_city", {
        "lat": lat, "lon": lon, "key": iqair_key
    })
    if "data" in res:
        pollution = res["data"]["current"]["pollution"]
        data.update({
            "air_quality_index": pollution.get("aqius"),
            "main_pollutant": pollution.get("mainus")
        })

    return data

# ---------- Example ----------
if __name__ == "__main__":
    lat, lon = 10.52, 76.21
    d = get_env_data(
        lat, lon,
        owm_key="ur api",
        weatherapi_key="ur api",
        iqair_key="ur api"
    )

    print("\n📊 Full Environmental + Soil + Air Data:")
    for k, v in d.items():
        print(f"{k}: {v}")

