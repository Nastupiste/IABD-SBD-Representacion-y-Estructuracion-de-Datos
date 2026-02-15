"""
# Utilizando Polars:
# PASO 2: Limpieza y Estructuración.
"""

import polars as pl
from .db_connector import get_polars_dataframe


def clean_data(raw_data):
    # TODO: Tratar nulos y datos inconsistentes.
    pass


"""
# PASO 3: Generación de Dataframes a partir de los datos limpios ---
# TODO: Crear nuevas columnas calculadas, ¿vale con lo que tenemos en get_stats?.
# TODO: Crear columnas agrupadas para segmentar la información por provincias, años o sectores. ¿Usamos años? Aunque ya usemos ID en get_stats().
# TODO: pasar los datos limpios en lugar de los originales.
"""


def get_hourly_weather(df):
    """Datos del tiempo extraidos por franja horaria."""
    return (
        df.select(["id", "payload"])
        .unnest("payload")
        .select(["id", "timestamp_captura", "hourly"])
        .unnest("hourly")
        .explode("data")
        .unnest("data")
    )


def get_current_weather(df):
    """Datos del tiempo actual."""
    return (
        df.sort("id", descending=True)  # Ordenamos por ID (el último insertado arriba)
        .limit(
            1
        )  # Nos quedamos solo con el primero, para coger el "current" de la fila más reciente
        .unnest("payload")
        .select(["timestamp_captura", "current"])
        .unnest("current")
    )


def get_stats(df):
    """
    Estadísticas por ID (máximo, mínimo, promedio de temperatura y total de precipitación diaria). Aquí se crean columnas nuevas,
    agrupando por ID para obtener estadísticas diarias.
    """
    return (
        df.select(["id", "payload"])
        .unnest("payload")
        .select(["id", "hourly"])
        .unnest("hourly")
        .explode("data")
        .unnest("data")
        .group_by("id")
        .agg(
            [
                pl.col("temperature").max().alias("temp_max"),
                pl.col("temperature").min().alias("temp_min"),
                pl.col("temperature").mean().alias("temp_avg"),
                pl.col("precipitation")
                .struct.field("total")
                .sum()
                .alias("precip_total_diaria"),
            ]
        )
    )


if __name__ == "__main__":

    df = get_polars_dataframe("openmeteo")

    if df is not None:

        df_hourly = get_hourly_weather(df)
        df_current = get_current_weather(df)
        df_stats = get_stats(df)

        print("--- VISTA DEL PRONÓSTICO POR HORAS ---")
        print(df_hourly.head(10))

        print("--- VISTA DEL CLIMA ACTUAL ---")
        print(df_current)

        print("--- VISTA DE ESTADÍSTICAS POR ID ---")
        print(df_stats.head(10))
