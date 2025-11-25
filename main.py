from scripts.mongo_connection import leer_todo
from scripts.extract_meteo import obtencion_datos_open_meteo
from scripts.extract_meteosource import obtencion_datos_api as obtencion_datos_meteo_source

leer_todo()

print("Ahora añadimos datos de ambas APIs")

obtencion_datos_open_meteo()

obtencion_datos_meteo_source()

leer_todo()
