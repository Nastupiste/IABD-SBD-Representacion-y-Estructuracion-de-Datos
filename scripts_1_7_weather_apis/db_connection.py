import os
import sqlite3
import json

# La base de datos está un nivel por encima de este script, en la raíz del proyecto:
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data.db")


def insert_data(table_name, data):
    """Guarda el diccionario 'data' en una tabla SQLite como texto JSON."""
    try:
        # Conexión a la base de datos (se crea si no existe)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Creamos la tabla si no existe
        # Guardamos el timestamp y el objeto completo como JSON para mantener la estructura original
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                payload TEXT
            )
        """
        )

        # Insertamos los datos
        timestamp = data.get("timestamp_captura")
        payload = json.dumps(data)  # Convertimos el diccionario a string JSON

        cursor.execute(
            f"INSERT INTO {table_name} (timestamp, payload) VALUES (?, ?)",
            (timestamp, payload),
        )

        conn.commit()
        conn.close()
        print(f"Datos guardados exitosamente en: {DB_PATH}")

    except sqlite3.Error as e:
        print(f"Error al guardar en SQLite: {e}")


def read_table(table_name):
    """Lee todos los registros de una tabla y los imprime formateados por terminal."""
    try:
        conn = sqlite3.connect(DB_PATH)
        # Esto permite acceder a las columnas por nombre como si fuera un diccionario
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Comprobamos primero si la tabla existe para evitar errores
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )
        if not cursor.fetchone():
            print(f"La tabla '{table_name}' no existe todavía.")
            return

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        print(f"\n--- CONTENIDO DE LA TABLA: {table_name} ---")
        for row in rows:
            # Convertimos el string JSON de nuevo a un diccionario de Python
            payload_dict = json.loads(row["payload"])

            print(f"ID: {row['id']} | Registro: {row['timestamp']}")
            # Usamos json.dumps con indent para que se vea bonito en terminal
            print(json.dumps(payload_dict, indent=4, ensure_ascii=False))
            print("-" * 40)

        conn.close()
    except sqlite3.Error as e:
        print(f"Error al leer de SQLite: {e}")
