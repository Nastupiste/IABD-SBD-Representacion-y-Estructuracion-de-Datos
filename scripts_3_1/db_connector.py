import polars as pl
import sqlite3
from scripts_1_7_weather_apis.db_connection import DB_PATH


def get_weather_schema():
    """Define el esquema exacto para el JSON de meteorología."""
    # Esquema para la precipitación (se repite en current y hourly)
    precip_schema = pl.Struct(
        [pl.Field("total", pl.Float64), pl.Field("type", pl.String)]
    )

    return pl.Struct(
        [
            pl.Field("lat", pl.String),
            pl.Field("lon", pl.String),
            pl.Field("timestamp_captura", pl.String),
            pl.Field(
                "current",
                pl.Struct(
                    [
                        pl.Field("temperature", pl.Float64),
                        pl.Field("summary", pl.String),
                        pl.Field("icon", pl.String),
                        pl.Field("cloud_cover", pl.Float64),
                        pl.Field(
                            "wind",
                            pl.Struct(
                                [
                                    pl.Field("speed", pl.Float64),
                                    pl.Field("angle", pl.Int64),
                                    pl.Field("dir", pl.String),
                                ]
                            ),
                        ),
                        pl.Field("precipitation", precip_schema),
                    ]
                ),
            ),
            pl.Field(
                "hourly",
                pl.Struct(
                    [
                        pl.Field(
                            "data",
                            pl.List(
                                pl.Struct(
                                    [
                                        pl.Field("date", pl.String),
                                        pl.Field("weather", pl.String),
                                        pl.Field("temperature", pl.Float64),
                                        pl.Field("summary", pl.String),
                                        pl.Field("precipitation", precip_schema),
                                    ]
                                )
                            ),
                        )
                    ]
                ),
            ),
        ]
    )


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
