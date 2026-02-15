from scripts_3_1.db_connector import get_polars_dataframe
from scripts_3_1.data_processor import (
    get_hourly_weather,
    get_current_weather,
    get_stats,
)


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
    start_step(
        "Paso 1: CONEXIÓN: Obtener un objeto de Polars con los datos de la tabla 'openmeteo' usando read_database."
    )

    df = get_polars_dataframe("openmeteo")
    if df is not None:
        print(df.head())

    end_step()

    start_step(
        "Paso 2: LIMPIEZA Y ESTRUCTURACIÓN CON POLARS: nulos, columnas calculadas y agrupaciones."
    )

    if df is not None:

        df_hourly = get_hourly_weather(df)
        df_current = get_current_weather(df)
        df_stats = get_stats(df)

        print("--- VISTA DEL PRONÓSTICO POR HORAS ---\n")
        print(df_hourly.head(10))

        print("\n--- VISTA DEL CLIMA ACTUAL ---\n")
        print(df_current)

        print("\n--- VISTA DE ESTADÍSTICAS POR ID ---\n")
        print(df_stats.head(10))

    end_step()

    start_step(
        "Paso 3: llamar a scripts_3_1/data_processor.py, create_columns() y structure_data()\npara crear nuevas columnas calculadas y agrupadas."
    )

    print("---- PENDIENTE ----")

    end_step()

    start_step(
        "Paso 4: llamar a scripts_3_1/visualizer.py para generar gráficos con Plotly."
    )

    print("---- PENDIENTE ----")

    end_step()


if __name__ == "__main__":
    main()
