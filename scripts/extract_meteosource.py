import time
import json
from datetime import datetime
from pymeteosource.api import Meteosource
from pymeteosource.types import tiers, sections, units, langs

# Variables
API_KEY = "kactprlujoa3p677acx480865izfqb0yvuer9ezb"
TIER = tiers.FREE
LAT = "37.3886"
LON = "-5.9823"

def obtencion_datos_api():
    try:
        meteosource = Meteosource(API_KEY, TIER)
    except Exception as e:
        print(f"Error al inicializar pymeteosource: {e}")
        return
    
    timestmap_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        forecast = meteosource.get_point_forecast(
            lat = float(LAT),
            lon = float(LON),
            sections=[sections.CURRENT, sections.HOURLY],
            units=units.METRIC,
            lang=langs.ENGLISH
        )

        current_data = {
            "temperature": forecast.current.temperature,
            "summary": forecast.current.summary,
            "icon": forecast.current.icon,
            "wind": {
                "speed": forecast.current.wind.speed,
                "angle": forecast.current.wind.angle,
                "dir": forecast.current.wind.dir
            },
            "precipitation": {
                "total": forecast.current.precipitation.total,
                "type": forecast.current.precipitation.type
            },
            "cloud_cover": forecast.current.cloud_cover
        }

        hourly_data = []
        for i, hour in enumerate(forecast.hourly):
            if i >= 12:
                break
            hourly_data.append({
                "date": str(hour.date),
                "weather": hour.weather,
                "temperature": hour.temperature,
                "summary": hour.summary,
                "precipitation": {
                    "total": hour.precipitation.total,
                    "type": hour.precipitation.type
                }
            })

        datos_finales = {
            "lat": LAT,
            "lon": LON,
            "timestamp_captura": timestmap_actual,
            "current": current_data,
            "hourly": {
                "data": hourly_data
            }
        }

        print(f"Ubicación: Sevilla")
        print(f"Temperatura: {forecast.current.temperature}ºC")
        print(f"Resumen: {forecast.current.summary}")
        print(f"Predicción futura: {len(hourly_data)} horas procesadas.")

        nombre_archivo = f"clima_sevilla_{int(time.time())}.json"
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_finales, f, indent=4, ensure_ascii=False)

        print(f"Datos guardados en {nombre_archivo}")

    except Exception as e:
        print(f"Error al obtener datos: {e}")

if __name__ == "__main__":
    obtencion_datos_api()
