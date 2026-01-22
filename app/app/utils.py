import requests


WIND_DIRS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
]


def fetch_venue_weather(location):
    lat, lng = location.y, location.x

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m",
        "timezone": "Asia/Bangkok",
        "wind_speed_unit": "ms"
    }

    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка запроса Open-Meteo для ({lat}, {lng}): {e}")

    current = data.get("current", {})

    pressure_hpa = current.get("surface_pressure", 1013.25)
    pressure_mmHg = round(pressure_hpa * 0.750062, 1)

    wind_deg = current.get("wind_direction_10m", 0)
    wind_dir = WIND_DIRS[int((wind_deg + 11.25) / 22.5) % 16]

    return {
        "temperature": current.get("temperature_2m", 0),
        "humidity": current.get("relative_humidity_2m", 0),
        "pressure": pressure_mmHg,
        "wind_speed": current.get("wind_speed_10m", 0),
        "wind_direction": wind_dir
    }