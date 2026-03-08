import polars as pl
import sqlite3
from scripts_1_7_weather_apis.db_connection import DB_PATH


def get_weather_schema():
    """Define el esquema exacto para el JSON real de Open-Meteo."""
    
    return pl.Struct([
        pl.Field("latitude", pl.Float64),
        pl.Field("longitude", pl.Float64),
        pl.Field("generationtime_ms", pl.Float64),
        pl.Field("utc_offset_seconds", pl.Int64),
        pl.Field("timezone", pl.String),
        pl.Field("timezone_abbreviation", pl.String),
        pl.Field("elevation", pl.Float64),
        # Sección 'current'
        pl.Field("current", pl.Struct([
            pl.Field("time", pl.String),
            pl.Field("interval", pl.Int64),
            pl.Field("temperature_2m", pl.Float64),
            pl.Field("weather_code", pl.Int64),
            pl.Field("wind_speed_10m", pl.Float64),
            pl.Field("wind_direction_10m", pl.Int64),
            pl.Field("precipitation", pl.Float64),
            pl.Field("cloud_cover", pl.Int64),
        ])),
        # Sección 'hourly' (Fíjate que aquí son listas de tipos simples)
        pl.Field("hourly", pl.Struct([
            pl.Field("time", pl.List(pl.String)),
            pl.Field("temperature_2m", pl.List(pl.Float64)),
            pl.Field("relative_humidity_2m", pl.List(pl.Int64)),
            pl.Field("apparent_temperature", pl.List(pl.Float64)),
            pl.Field("precipitation", pl.List(pl.Float64)),
            pl.Field("precipitation_probability", pl.List(pl.Int64)),
            pl.Field("weather_code", pl.List(pl.Int64)),
        ]))
    ])


def get_polars_dataframe(table_name):
    """
    Obtener un DataFrame de Polars a partir de una tabla en SQLite, decodificando el JSON con un esquema manual.
    """
    query = f"SELECT * FROM {table_name}"
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pl.read_database(query=query, connection=conn)
        conn.close()

        if not df.is_empty():
            schema = get_weather_schema()
            # 1. Decodificar el JSON con el esquema manual
            df = df.with_columns(
                pl.col("payload").str.json_decode(dtype=schema)
            ).unnest("payload")
            return df
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    df = get_polars_dataframe("openmeteo")

    if df is not None:
        print(df)
