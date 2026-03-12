from scripts_1_7_weather_apis.db_connection import read_table
from scripts_1_7_weather_apis.extract_openmeteo import get_open_meteo
from scripts_3_1.db_connector import get_polars_df_from_last_fetch
from scripts_3_1.data_processor import (
    get_hourly_weather_dataframe,
    get_current_weather_dataframe,
    get_stats_dataframe,
)
from scripts_3_1.visualizer import plot_combined_dashboard

TABLES = [
    "openmeteo",
]


def get_new_data():
    print("\n\n --- Pidiendo nuevos datos a la API de OpenMeteo --- \n\n")
    get_open_meteo()


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

    get_new_data()

    start_step(
        "Paso 1: CONEXIÓN: Obtener un objeto de Polars con los datos de la tabla 'openmeteo' usando read_database."
    )

    df = get_polars_df_from_last_fetch("openmeteo")
    if df is not None:
        print(df)

    end_step()

    start_step(
        "Pasos 2 y 3: LIMPIEZA Y ESTRUCTURACIÓN CON POLARS: limpiar nulos e inconsistencias, añadir columnas calculadas y agrupaciones."
    )

    if df is not None:

        df_hourly = get_hourly_weather_dataframe(df)

        print("--- VISTA DEL PRONÓSTICO POR HORAS ---\n")
        print(df_hourly.head(10))

        df_current = get_current_weather_dataframe(df)

        print("\n--- VISTA DEL CLIMA ACTUAL ---\n")
        print(df_current)

        df_stats = get_stats_dataframe(df)

        print("\n--- VISTA DE ESTADÍSTICAS DIARIAS ---\n")
        print(df_stats.head(10))

    end_step()

    start_step("Paso 4: ANÁLISIS VISUAL CON PLOTLY.")

    print("Abriendo dashboard combinado con 4 gráficos diferentes...")

    plot_combined_dashboard()

    end_step()


if __name__ == "__main__":
    main()
