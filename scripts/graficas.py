import os
import math
from datetime import datetime
import matplotlib.pyplot as plt
from .mongo_connection import read_data

OUTPUT_DIR = "graficas"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def parse_timestamp(ts: str):
    """
    Intenta convertir '2025-11-25 19:53:55' a datetime.
    Si falla, devuelve None.
    """
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def get_latest_document(documents):
    """
    Devuelve el documento más reciente usando 'timestamp_captura'.
    Si no se puede parsear, devuelve el último de la lista.
    """
    docs_with_dt = []
    for d in documents:
        ts_str = d.get("timestamp_captura")
        dt = parse_timestamp(ts_str) if ts_str else None
        if dt:
            docs_with_dt.append((dt, d))

    if docs_with_dt:
        docs_with_dt.sort(key=lambda x: x[0])
        return docs_with_dt[-1][1]  # el más reciente
    elif documents:
        return documents[-1]
    else:
        return None


# ---------- GRÁFICAS ----------


def plot_temperature_hourly(doc, collection_name: str, ts_str: str):
    """Genera un gráfico de línea con la evolución de la temperatura por hora.
    Usa los datos horarios (hourly.data)"""
    hourly = doc.get("hourly", {}).get("data", [])
    if not hourly:
        print(f"[{collection_name}] Sin datos horarios para temperatura.")
        return

    horas = [
        item["date"][11:16] for item in hourly
    ]  # '2025-11-25 18:00:00+00:00' -> '18:00'
    temps = [item.get("temperature") for item in hourly]

    plt.figure(figsize=(10, 4))
    plt.plot(horas, temps, marker="o")
    plt.title(f"Temperatura por hora - {collection_name}")
    plt.xlabel("Hora")
    plt.ylabel("Temperatura (°C)")
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.tight_layout()
    filename = os.path.join(
        OUTPUT_DIR, f"{collection_name}_{ts_str}_temperatura_horaria.jpg"
    )
    plt.savefig(filename, dpi=200)
    plt.close()
    print(f"Guardado {filename}")


def plot_precipitation_hourly(doc, collection_name: str, ts_str: str):
    """Crea un gráfico de barras con la precipitación prevista por hora.
    Muestra los milímetros de lluvia en cada intervalo horario."""
    hourly = doc.get("hourly", {}).get("data", [])
    if not hourly:
        print(f"[{collection_name}] Sin datos horarios de precipitación.")
        return

    horas = [item["date"][11:16] for item in hourly]
    prec = [item.get("precipitation", {}).get("total", 0.0) for item in hourly]

    plt.figure(figsize=(10, 4))
    plt.bar(horas, prec)
    plt.title(f"Precipitación por hora - {collection_name}")
    plt.xlabel("Hora")
    plt.ylabel("Precipitación (mm)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    filename = os.path.join(
        OUTPUT_DIR, f"{collection_name}_{ts_str}_precipitacion_horaria.jpg"
    )
    plt.savefig(filename, dpi=200)
    plt.close()
    print(f"Guardado {filename}")


def plot_cloud_cover(doc, collection_name: str, ts_str: str):
    """Dibuja una barra única mostrando el porcentaje de cobertura de nubes actual.
    Representa el valor de current.cloud_cover entre 0 y 100%."""
    current = doc.get("current", {})
    cloud = current.get("cloud_cover")
    if cloud is None:
        print(f"[{collection_name}] Sin dato de cloud_cover.")
        return

    plt.figure(figsize=(4, 4))
    plt.bar(["Cobertura de nubes"], [cloud])
    plt.title(f"Cobertura de nubes actual - {collection_name}")
    plt.ylim(0, 100)
    plt.ylabel("%")

    plt.tight_layout()
    filename = os.path.join(OUTPUT_DIR, f"{collection_name}_{ts_str}_cloud_cover.jpg")
    plt.savefig(filename, dpi=200)
    plt.close()
    print(f"Guardado {filename}")


def plot_wind(doc, collection_name: str, ts_str: str):
    """Genera un gráfico polar con la dirección y velocidad del viento actual.
    Muestra un único vector según wind.angle y wind.speed."""
    current = doc.get("current", {})
    wind = current.get("wind", {})
    speed = wind.get("speed")
    angle_deg = wind.get("angle")

    if speed is None or angle_deg is None:
        print(f"[{collection_name}] Sin datos suficientes de viento.")
        return

    angle_rad = math.radians(angle_deg)

    plt.figure(figsize=(5, 5))
    ax = plt.subplot(111, polar=True)
    ax.bar(angle_rad, speed, width=math.radians(20))
    ax.set_title(f"Viento actual - {collection_name}")

    filename = os.path.join(OUTPUT_DIR, f"{collection_name}_{ts_str}_viento.jpg")
    plt.savefig(filename, dpi=200)
    plt.close()
    print(f"Guardado {filename}")


# ---------- ORQUESTADOR PARA UNA COLECCIÓN ----------


def generate_plots_for_collection(collection_name: str):
    print(f"\n=== Procesando colección: {collection_name} ===")
    docs = read_data(collection_name)

    if not docs:
        print(f"[{collection_name}] No se encontraron documentos.")
        return

    doc = get_latest_document(docs)
    if not doc:
        print(f"[{collection_name}] No se pudo determinar el documento más reciente.")
        return

    doc = get_latest_document(docs)
    if not doc:
        print(f"[{collection_name}] No se pudo determinar el documento más reciente.")
        return

    # Obtener timestamp seguro para incluir en el nombre del archivo
    ts = parse_timestamp(doc["timestamp_captura"])
    ts_str = ts.strftime("%Y%m%d_%H%M%S") if ts else "sin_timestamp"

    # Generar todas las gráficas sencillas
    plot_temperature_hourly(doc, collection_name, ts_str)
    plot_precipitation_hourly(doc, collection_name, ts_str)
    plot_cloud_cover(doc, collection_name, ts_str)
    plot_wind(doc, collection_name, ts_str)


# ---------- MAIN ----------

if __name__ == "__main__":
    # Ajusta aquí los nombres reales de tus colecciones
    collections = [
        "openmeteo",
        "meteosource",
    ]

    for col in collections:
        generate_plots_for_collection(col)
