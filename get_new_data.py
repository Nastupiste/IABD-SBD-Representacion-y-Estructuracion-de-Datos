from scripts_1_7_weather_apis.db_connection import read_table
from scripts_1_7_weather_apis.extract_meteo import get_open_meteo
from scripts_1_7_weather_apis.extract_meteosource import get_meteosource

TABLES = [
    "openmeteo",
    "meteosource",
]

print("Datos guardados:")

for table in TABLES:
    read_table(table)

print("\n\n --- Pidiendo nuevos datos a ambas APIs --- \n\n")

get_open_meteo()

get_meteosource()

print("\n --- \nDatos actualizados:")

for table in TABLES:
    read_table(table)
