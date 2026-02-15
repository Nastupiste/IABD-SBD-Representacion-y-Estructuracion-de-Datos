import os
import polars as pl
from datetime import datetime
from scripts_1_7_weather_apis.db_connection import BASE_DIR
from .db_connector import get_polars_dataframe

"""
# Utilizando Polars:
# PASO 2: Limpieza y Estructuración
# - Eliminar filas con nulos: en clean_nulls eliminamos filas con valores nulos en columnas clave (ID, timestamp_captura).
# - Eliminamos filas con datos horarios nulos.
# - get_hourly_weather_dataframe: limpiamos nulos en la precipitación (asumimos 0.0 y "none" si es nulo) y en la temperatura (forward fill). También filtramos temperaturas extremas.
# - get_stats_dataframe: eliminamos filas con temperaturas nulas y contamos los nulos en precipitación como 0 para el total diario.
# - get_current_weather_dataframe: filtramos solo filas donde 'current' no es nulo, y limpiamos nulos en precipitación y viento con valores por defecto (0 o "unknown").
"""


def clean_nulls(df):
    """
    Paso intermedio para limpiar el dataframe base de nulos antes de ramificar.
    """
    return df.drop_nulls(subset=["id", "timestamp_captura"])


"""
# PASO 3: Generación de Dataframes a partir de los datos limpios ---
# - Crear nuevas columnas calculadas: en df_stats, calculamos temperatura máxima, mínima y promedio.
# - Crear columnas agrupadas para segmentar la información por provincias, años o sectores: en df_stats agrupamos por ID.
# - Capa de plata (silver layer): exportar a CSV los dataframes limpios.
"""


def export_to_csv(df, filename):
    """Exportar un DataFrame de Polars a CSV."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")  # AñoMesDia_HoraMinuto
    output_dir = f"{BASE_DIR}/data/silver_layer"  # Directorio de salida para los CSVs
    os.makedirs(output_dir, exist_ok=True)  # Crear el directorio si no existe

    full_path = f"{output_dir}/{filename}_{timestamp}.csv"

    df.write_csv(full_path)
    print(f"Archivo exportado correctamente: {full_path}")


def get_hourly_weather_dataframe(df):
    """Datos del tiempo extraidos por franja horaria."""
    df = clean_nulls(df)
    df_hourly = (
        df.select(["id", "timestamp_captura", "hourly"])
        .drop_nulls("hourly")  # LIMPIEZA: Eliminar filas donde 'hourly' es nulo.
        .unnest("hourly")
        .explode("data")
        .unnest("data")
        .with_columns(  # Aplanamos el último nivel (precipitación) para que el CSV no de error
            [
                # LIMPIEZA: Si la precipitación es nula, asumimos total 0.0 y tipo "none".
                pl.col("precipitation")
                .struct.field("total")
                .fill_null(0.0)
                .alias("precip_total"),
                pl.col("precipitation")
                .struct.field("type")
                .fill_null("none")
                .alias("precip_type"),
                # LIMPIEZA: Si la temperatura es nula, rellenamos con el valor anterior (forward fill).
                pl.col("temperature").fill_null(strategy="forward"),
            ]
        )
        # LIMPIEZA: Validar temperaturas extremas (entre -60 y 60 grados, elimina registros inconsistentes).
        .filter(pl.col("temperature").is_between(-60, 60))
        .drop("precipitation")
    )
    export_to_csv(df_hourly, "Tiempo_por_horas")
    return df_hourly


def get_current_weather_dataframe(df):
    """Datos del tiempo actual."""
    df = clean_nulls(df)
    df_current = (
        df.sort("id", descending=True)
        .filter(
            pl.col("current").is_not_null()
        )  # LIMPIEZA: Filtrar solo filas donde 'current' no es nulo.
        .limit(1)
        .drop_nulls("hourly")  # LIMPIEZA: Eliminar filas donde 'hourly' es nulo.
        .select(["timestamp_captura", "current"])
        .unnest("current")
        .with_columns(  # Aplanamos el último nivel (precipitación y viento) para que el CSV no de error
            [
                pl.col("precipitation")
                .struct.field("total")
                .fill_null(0)
                .alias("precip_total"),
                pl.col("precipitation")
                .struct.field("type")
                .fill_null("unknown")
                .alias("precip_type"),
                pl.col("wind").struct.field("speed").fill_null(0).alias("wind_speed"),
                pl.col("wind").struct.field("angle").fill_null(0).alias("wind_angle"),
                pl.col("wind")
                .struct.field("dir")
                .fill_null("unknown")
                .alias("wind_dir"),
            ]
        )
        .drop(["precipitation", "wind"])
    )
    # El sort de arriba es para obtener el registro más reciente, ya que ID es incremental.
    export_to_csv(df_current, "Tiempo_actual")
    return df_current


def get_stats_dataframe(df):
    """
    Estadísticas por ID (máximo, mínimo, promedio de temperatura y total de precipitación diaria). Aquí se crean columnas nuevas,
    agrupando por ID para obtener estadísticas diarias.
    """
    df = clean_nulls(df)
    df_stats = (
        df.select(["id", "hourly"])
        .drop_nulls("hourly")  # LIMPIEZA: Eliminar filas donde 'hourly' es nulo.
        .unnest("hourly")
        .explode("data")
        .unnest("data")
        # LIMPIEZA: Antes de agrupar, eliminamos filas con temperaturas nulas.
        .filter(pl.col("temperature").is_not_null())
        .group_by("id")
        .agg(
            [
                pl.col("temperature")
                .max()
                .alias("temp_max"),  # Columna calculada para la temperatura máxima.
                pl.col("temperature")
                .min()
                .alias("temp_min"),  # Columna calculada para la temperatura mínima.
                pl.col("temperature")
                .mean()
                .round(2)
                .alias("temp_avg"),  # Columna calculada para la temperatura promedio.
                # LIMPIEZA: sum() maneja nulls como 0 si usamos fill_null antes
                pl.col("precipitation")
                .struct.field("total")
                .fill_null(0)
                .sum()
                .alias("precip_total_diaria"),
            ]
        )
    )

    export_to_csv(df_stats, "Estadísticas_diarias_por_ID")

    return df_stats


if __name__ == "__main__":

    df = get_polars_dataframe("openmeteo")

    if df is not None:

        df_hourly = get_hourly_weather_dataframe(df)
        df_current = get_current_weather_dataframe(df)
        df_stats = get_stats_dataframe(df)

        print("--- VISTA DEL PRONÓSTICO POR HORAS ---")
        print(df_hourly.head(10))

        print("--- VISTA DEL CLIMA ACTUAL ---")
        print(df_current)

        print("--- VISTA DE ESTADÍSTICAS POR ID ---")
        print(df_stats.head(10))
