from scripts_1_7_weather_apis.db_connection import read_table
from scripts_1_7_weather_apis.extract_openmeteo import get_open_meteo
from scripts_1_7_weather_apis.extract_meteosource import get_meteosource
from scripts_3_1.db_connector import get_polars_dataframe
from scripts_3_1.data_processor import (
    get_hourly_weather_dataframe,
    get_current_weather_dataframe,
    get_stats_dataframe,
)

TABLES = [
    "openmeteo",
    # "meteosource",
]


def get_new_data():
    print("Datos guardados:")

    for table in TABLES:
        read_table(table)

    # print("\n\n --- Pidiendo nuevos datos a ambas APIs --- \n\n")
    print("\n\n --- Pidiendo nuevos datos a la API de OpenMeteo --- \n\n")

    get_open_meteo()

    get_meteosource()

    print("\n --- \nDatos actualizados:")

    for table in TABLES:
        read_table(table)


def start_step(description):
    print("\n")
    print("-" * 120)
    print(description)
    print("-" * 120)
    print("\n")


def end_step():
    print("\n")
    print("-" * 120)


def main():

    print("INICIO DEL PROCESO DE ANÁLISIS DE DATOS CLIMÁTICOS\n")
    print(
        "La base de datos debe tener datos ya, si no es así, descomentar la siguiente línea:"
    )

    # get_new_data()

    start_step(
        "Paso 1: CONEXIÓN: Obtener un objeto de Polars con los datos de la tabla 'openmeteo' usando read_database."
    )

    df = get_polars_dataframe("openmeteo")
    if df is not None:
        print(df.head())

    end_step()

    start_step(
        "Pasos 2 y 3: LIMPIEZA Y ESTRUCTURACIÓN CON POLARS: limpiar nulos e inconsistencias, añadir columnas calculadas y agrupaciones."
    )

    if df is not None:

        df_hourly = get_hourly_weather_dataframe(df)
        df_current = get_current_weather_dataframe(df)
        df_stats = get_stats_dataframe(df)

        print("--- VISTA DEL PRONÓSTICO POR HORAS ---\n")
        print(df_hourly.head(10))

        print("\n--- VISTA DEL CLIMA ACTUAL ---\n")
        print(df_current)

        print("\n--- VISTA DE ESTADÍSTICAS POR ID ---\n")
        print(df_stats.head(10))

    end_step()

    start_step("Paso 4: ANÁLISIS VISUAL CON PLOTLY.")

    print("---- PENDIENTE ----")

    end_step()


if __name__ == "__main__":
    main()
