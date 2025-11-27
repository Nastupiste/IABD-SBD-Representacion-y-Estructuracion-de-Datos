from scripts.mongo_connection import leer_todo
from scripts.extract_meteo import obtencion_datos_open_meteo
from scripts.extract_meteosource import (
    obtencion_datos_api as obtencion_datos_meteo_source,
)
from scripts.graficas import generate_plots_for_collection

COLECCIONES_MONGO = [
    "openmeteo",
    "meteosource",
]

print("Datos iniciales:")

leer_todo()

print("\n --- \nAñadimos datos de ambas APIs:\n --- \n")

obtencion_datos_open_meteo()

obtencion_datos_meteo_source()

print("\n --- \nDatos tras la adición:")

leer_todo()

for coleccion in COLECCIONES_MONGO:
    generate_plots_for_collection(coleccion)
