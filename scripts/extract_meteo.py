import requests
from datetime import datetime
from .mongo_connection import insert_data

LAT = "37.3886" 
LON = "-5.9823"
URL = "https://api.open-meteo.com/v1/forecast"
COLLECTION_NAME = "openmeteo"


def get_wind_dir(degrees):
    """Convierte grados a dirección cardinal (N, NNE, etc.)"""
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
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


def obtencion_datos_open_meteo():
    timestamp_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Pedimos los campos necesarios para reconstruir tu JSON
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current": "temperature_2m,weather_code,wind_speed_10m,wind_direction_10m,precipitation,cloud_cover",
        "hourly": "temperature_2m,weather_code,precipitation,rain,showers,snowfall",
        "timezone": "auto",
        "forecast_days": 1
    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status() # Lanza error si falla la petición HTTP
        data = response.json()
        
        # 1. Procesar CURRENT
        curr_raw = data["current"]
        w_slug, w_summary = get_weather_translation(curr_raw["weather_code"])
        
        # Simulación de tipo de precipitación en current (Open-Meteo solo da 'precipitation' genérico en current simple)
        # Asumimos lluvia si hay precipitación y la temperatura es > 0
        curr_precip_type = "none"
        if curr_raw["precipitation"] > 0:
            curr_precip_type = "rain" 

        current_data = {
            "temperature": curr_raw["temperature_2m"],
            "summary": w_summary,
            "icon": w_slug, # Usamos el slug como 'icon'
            "wind": {
                "speed": curr_raw["wind_speed_10m"],
                "angle": curr_raw["wind_direction_10m"],
                "dir": get_wind_dir(curr_raw["wind_direction_10m"]) 
            },
            "precipitation": {
                "total": curr_raw["precipitation"],
                "type": curr_precip_type
            },
            "cloud_cover": curr_raw["cloud_cover"]
        }

        # 2. Procesar datos
        hourly_raw = data["hourly"]
        hourly_data = []
        
        limit = 12 
        
        for i in range(min(len(hourly_raw["time"]), limit)):
            h_slug, h_summary = get_weather_translation(hourly_raw["weather_code"][i])
            
            # Lógica para tipo de precipitación más precisa aquí
            p_total = hourly_raw["precipitation"][i]
            p_type = get_precip_type(
                hourly_raw["rain"][i], 
                hourly_raw["snowfall"][i], 
                hourly_raw["showers"][i]
            )

            hourly_data.append({
                "date": hourly_raw["time"][i],
                "weather": h_slug,
                "temperature": hourly_raw["temperature_2m"][i],
                "summary": h_summary,
                "precipitation": {
                    "total": p_total,
                    "type": p_type
                }
            })

        # JSON Final
        datos_finales = {
            "lat": LAT,
            "lon": LON,
            "timestamp_captura": timestamp_actual,
            "current": current_data,
            "hourly": {
                "data": hourly_data
            }
        }

        # Insertar datos en MongoDB
        insert_data(COLLECTION_NAME, datos_finales)

    except Exception as e:
        print(f"Error al obtener datos de Open-Meteo: {e}")

if __name__ == "__main__":
    obtencion_datos_open_meteo()