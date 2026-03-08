import requests
from datetime import datetime, timezone
from .db_connection import insert_data

LAT = "37.3886"
LON = "-5.9823"
URL = "https://api.open-meteo.com/v1/forecast"
COLLECTION_NAME = "openmeteo"


def get_wind_dir(degrees):
    """Convierte grados a dirección cardinal (N, NNE, etc.)"""
    dirs = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    ix = int((degrees + 11.25) / 22.5)
    return dirs[ix % 16]


def get_weather_translation(wmo_code):

    # Traduce el código WMO de Open-Meteo al estilo de texto de Meteosource.
    # Mapeo simplificado para traducir la respuesta.
    if wmo_code == 0:
        return "sunny", "Sunny"
    if wmo_code in [1, 2]:
        return "partly_sunny", "Partly sunny"
    if wmo_code == 3:
        return "overcast", "Overcast"
    if 45 <= wmo_code <= 48:
        return "fog", "Fog"
    if 51 <= wmo_code <= 67:
        return "rain", "Rain"
    if 71 <= wmo_code <= 77:
        return "snow", "Snow"
    if 80 <= wmo_code <= 82:
        return "rain_shower", "Rain showers"
    if 95 <= wmo_code <= 99:
        return "thunderstorm", "Thunderstorm"
    return "cloudy", "Cloudy"


def get_precip_type(rain_val, snow_val, showers_val):
    """Determina el tipo de precipitación basado en los valores"""
    total = rain_val + snow_val + showers_val
    if total == 0:
        return "none"
    if snow_val > 0:
        return "snow"
    return "rain"


def get_open_meteo():
    timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    params = {
        "latitude": LAT,
        "longitude": LON,
        "current": "temperature_2m,weather_code,wind_speed_10m,wind_direction_10m,precipitation,cloud_cover",
        "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,precipitation_probability,weather_code",
        "timezone": "auto",
        "forecast_days": 7,
    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()

        # 1. Procesar CURRENT
        curr_raw = data["current"]
        w_slug, w_summary = get_weather_translation(curr_raw["weather_code"])

        # Deducimos el tipo basándonos en el código WMO
        # Los códigos 71-77 son nieve.
        curr_precip_type = "none"
        if curr_raw["precipitation"] > 0:
            curr_precip_type = "snow" if 71 <= curr_raw["weather_code"] <= 77 else "rain"

        current_data = {
            "temperature": curr_raw["temperature_2m"],
            "summary": w_summary,
            "icon": w_slug,
            "wind": {
                "speed": curr_raw["wind_speed_10m"],
                "angle": curr_raw["wind_direction_10m"],
                "dir": get_wind_dir(curr_raw["wind_direction_10m"]),
            },
            "precipitation": {
                "total": curr_raw["precipitation"],
                "type": curr_precip_type,
            },
            "cloud_cover": curr_raw["cloud_cover"],
        }

        # 2. Procesar HOURLY
        hourly_raw = data["hourly"]
        hourly_data = []

        for i in range(len(hourly_raw["time"])):
            w_code = hourly_raw["weather_code"][i]
            p_total = hourly_raw["precipitation"][i]
            
            h_slug, h_summary = get_weather_translation(w_code)

            # Lógica de tipo de precipitación simplificada sin 'rain' ni 'snowfall'
            p_type = "none"
            if p_total > 0:
                # Si el código WMO indica nieve (71, 73, 75, 77, 85, 86)
                if w_code in [71, 73, 75, 77, 85, 86]:
                    p_type = "snow"
                else:
                    p_type = "rain"

            hourly_data.append({
                "date": str(datetime.fromisoformat(hourly_raw["time"][i]).replace(tzinfo=timezone.utc)),
                "weather": h_slug,
                "temperature": hourly_raw["temperature_2m"][i],
                "summary": h_summary,
                "precipitation": {"total": p_total, "type": p_type},
            })

        # JSON Final (Estructura que espera tu esquema de Polars)
        datos_finales = {
            "lat": str(LAT),
            "lon": str(LON),
            "timestamp_captura": timestamp_actual,
            "current": current_data,
            "hourly": {"data": hourly_data}, # Mantenemos el nivel 'data' para tu esquema original
        }

        insert_data(COLLECTION_NAME, datos_finales)

    except Exception as e:
        print(f"Error al obtener datos de Open-Meteo: {e}")


if __name__ == "__main__":
    get_open_meteo()
