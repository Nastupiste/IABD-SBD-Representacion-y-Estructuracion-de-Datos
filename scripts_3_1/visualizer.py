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
    "DAILY_STATS": BASE_PATH
    / "data_output"
    / "silver_layer"
    / "Estadísticas_diarias.csv",
    "HOURLY_WEATHER": BASE_PATH
    / "data_output"
    / "silver_layer"
    / "Tiempo_por_horas.csv",
    "CURRENT_WEATHER": BASE_PATH / "data_output" / "silver_layer" / "Tiempo_actual.csv",
}


def plot_daily_evolution():
    """Gráfico de líneas para la evolución de temperaturas diarias."""
    df = pl.read_csv(DIRS["DAILY_STATS"])

    # En Polars usamos 'unpivot' (antes 'melt') para pasar de ancho a largo
    # Esto permite que Plotly pinte varias líneas automáticamente con 'color'
    df_long = df.unpivot(
        index="date_no_time",
        on=["temp_max", "temp_avg", "temp_min"],
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


def plot_temp_distribution():
    """Histograma para ver la frecuencia de las temperaturas horarias."""
    df = pl.read_csv(DIRS["HOURLY_WEATHER"])

    fig = px.histogram(
        df,
        x="temperature",
        nbins=15,
        title="Distribución de Frecuencia Térmica",
        labels={"temperature": "Temperatura (°C)", "count": "Frecuencia (Horas)"},
        color_discrete_sequence=["#636EFA"],  # Un azul constante
        opacity=0.75,
        template="plotly_white",
    )

    # Añadimos una línea vertical con la media para dar más contexto
    mean_temp = df["temperature"].mean()
    fig.add_vline(
        x=mean_temp,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Media: {mean_temp:.1f}°C",
    )

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
    fig3 = plot_temp_distribution()
    fig4 = plot_wind_rose()

    # Crear una estructura de 1 fila y 2 columnas
    combined_fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Evolución",
            "Correlación",
            "Distribución de Temperatura",
            "Viento",
        ),
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

    # Subplot 1,1 (Evolución)
    combined_fig.update_xaxes(title_text="Fecha", row=1, col=1)
    combined_fig.update_yaxes(title_text="Temp (°C)", row=1, col=1)

    # Subplot 1,2 (Correlación)
    combined_fig.update_xaxes(title_text="Temp. Media (°C)", row=1, col=2)
    combined_fig.update_yaxes(title_text="Lluvia (mm)", row=1, col=2)

    # Subplot 2,1 (Distribución)
    combined_fig.update_xaxes(title_text="Temperatura (°C)", row=2, col=1)
    combined_fig.update_yaxes(title_text="Frecuencia (Horas)", row=2, col=1)

    # Subplot 2,2 (Viento - Polar)
    # Nota: Los gráficos polares usan 'angularaxis' y 'radialaxis'
    combined_fig.update_polars(radialaxis_title_text="Velocidad", row=2, col=2)

    combined_fig.update_layout(
        title={
            "text": "<b>DASHBOARD METEOROLÓGICO</b>",
            "x": 0.5,  # Posición horizontal (0.5 es el centro)
            "xanchor": "center",  # Ancla el texto al centro
            "font": {"size": 28, "family": "Arial"},
        },
        showlegend=True,
    )
    # include_plotlyjs='cdn' hace que el archivo pese mucho menos al cargar la librería desde la web
    combined_fig.write_html("plots.html", include_plotlyjs="cdn")

    print("Reporte exportado con éxito en: plots.html")
    combined_fig.show()


if __name__ == "__main__":
    # Ejemplo de uso:
    plot_combined_dashboard()
