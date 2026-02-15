from pathlib import Path
import polars as pl
import plotly.express as px
from plotly.subplots import make_subplots
from scripts_1_7_weather_apis.db_connection import BASE_DIR

"""
# PASO 4: Gráficos con Plotly.
"""

BASE_PATH = Path(BASE_DIR)

DIRS = {
    "DAILY_STATS": BASE_PATH / "data" / "silver_layer" / "Estadísticas_diarias.csv",
    "HOURLY_WEATHER": BASE_PATH / "data" / "silver_layer" / "Tiempo_por_horas.csv",
    "CURRENT_WEATHER": BASE_PATH / "data" / "silver_layer" / "Tiempo_actual.csv",
}


def plot_daily_evolution():
    """Gráfico de líneas para la evolución de temperaturas diarias."""
    df = pl.read_csv(DIRS["DAILY_STATS"])

    # En Polars usamos 'unpivot' (antes 'melt') para pasar de ancho a largo
    # Esto permite que Plotly pinte varias líneas automáticamente con 'color'
    df_long = df.unpivot(
        index="date_no_time",
        on=["temp_max", "temp_min", "temp_avg"],
        variable_name="Metrica",
        value_name="Temperatura",
    )

    fig = px.line(
        df_long,
        x="date_no_time",
        y="Temperatura",
        color="Metrica",
        title="Evolución de Temperaturas Diarias",
        labels={
            "date_no_time": "Fecha",
            "Temperatura": "Temp (°C)",
            "Metrica": "Indicador",
        },
        markers=True,
        template="plotly_white",
    )
    return fig


def plot_correlation():
    """Scatter plot para ver la relación entre temperatura y lluvia."""
    df = pl.read_csv(DIRS["DAILY_STATS"])

    fig = px.scatter(
        df,
        x="temp_avg",
        y="precip_total_diaria",
        size="temp_max",
        color="temp_min",
        hover_data=["date_no_time"],
        title="Correlación: Temp. Media vs Precipitación",
        labels={
            "temp_avg": "Temp. Media (°C)",
            "precip_total_diaria": "Lluvia (mm)",
            "temp_min": "Mínima",
            "temp_max": "Máxima",
        },
        template="plotly_white",
    )
    return fig


def plot_hourly_facets():
    """Gráficos facetados para comparar la evolución según el estado del cielo."""
    df = pl.read_csv(DIRS["HOURLY_WEATHER"])

    # Convertimos la columna date a datetime real en Polars
    df = df.with_columns(pl.col("date").str.to_datetime(time_zone="UTC"))

    fig = px.line(
        df,
        x="date",
        y="temperature",
        facet_col="summary",  # Crea un gráfico por cada tipo de clima (Sunny, Partly Sunny...)
        facet_col_wrap=3,  # Máximo 3 columnas de gráficos
        title="Evolución Horaria segmentada por Clima",
        labels={"date": "Hora", "temperature": "Temp (°C)"},
        template="plotly_white",
    )
    # Ajustamos para que los ejes X sean independientes si se desea
    fig.update_xaxes(matches=None)
    return fig


def plot_wind_rose():
    """Rosa de los vientos utilizando los datos del tiempo actual."""
    df = pl.read_csv(DIRS["CURRENT_WEATHER"])

    fig = px.bar_polar(
        df,
        r="wind_speed",
        theta="wind_angle",
        color="temperature",
        title="Dirección y Velocidad del Viento (Actual)",
        labels={"wind_speed": "Velocidad", "wind_angle": "Grados"},
        template="plotly_white",
    )
    return fig


def plot_combined_dashboard():
    fig1 = plot_daily_evolution()
    fig2 = plot_correlation()
    fig3 = plot_hourly_facets()
    fig4 = plot_wind_rose()

    # Crear una estructura de 1 fila y 2 columnas
    combined_fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Evolución", "Correlación", "Evolución Horaria", "Viento"),
        specs=[
            [{"type": "xy"}, {"type": "xy"}],
            [{"type": "xy"}, {"type": "polar"}],
        ],  # La 4ª es polar para la rosa de los vientos
    )

    # Añadir las trazas de los gráficos de Plotly Express al subplot
    for trace in fig1.data:
        combined_fig.add_trace(trace, row=1, col=1)
    for trace in fig2.data:
        combined_fig.add_trace(trace, row=1, col=2)
    for trace in fig3.data:
        combined_fig.add_trace(trace, row=2, col=1)
    for trace in fig4.data:
        combined_fig.add_trace(trace, row=2, col=2)

    combined_fig.update_annotations(
        patch=dict(yshift=20)
    )  # Subir 20px lso títulos de los subplots para que no se solapen con las leyendas

    combined_fig.update_layout(title_text="Dashboard Meteorológico")
    combined_fig.show()


if __name__ == "__main__":
    # Ejemplo de uso:
    plot_combined_dashboard()
