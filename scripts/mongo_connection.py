import os
import json
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient

load_dotenv()  # Cargar variables del archivo .env
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
OPENMETEO = "openmeteo"
METEOSOURCE = "meteosource"

# Generamos un cliente con las credenciales de conexión del .env
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]  # Seleccionamos la base de datos


def test_connection():
    """
    Prueba la conexión a la base de datos.
    """
    try:
        client.admin.command("ping")
        print("Conexión exitosa a la base de datos MongoDB")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")


def read_data(collection_name: str, filtro: dict = None):
    """
    Lee documentos de una colección de MongoDB.
    - collection_name: nombre de la colección
    - filtro: diccionario opcional para filtrar resultados (default: todos)

    Retorna una lista de documentos.
    """
    try:
        collection = db[collection_name]

        if filtro is None:
            filtro = {}

        documentos = list(collection.find(filtro))

        # Convertir ObjectId a str para evitar problemas al serializar
        for doc in documentos:
            if "_id" in doc and isinstance(doc["_id"], ObjectId):
                doc["_id"] = str(doc["_id"])

        return documentos

    except Exception as e:
        print(f"Error leyendo datos de MongoDB ({collection_name}): {e}")
        return []

def leer_todo():
    """
    Lee datos de ambas colecciones en MongoDB.
    Retorna un diccionario con listas de documentos.
    """
    datos_openmeteo = read_data(OPENMETEO)
    print(f"======== DOCUMENTOS EN 'OPENMETEO': {len(datos_openmeteo)} ========")
    if len(datos_openmeteo) > 0:
        for i, doc in enumerate(datos_openmeteo):
            print(f"==== DOCUMENTO {i+1} ({doc['timestamp_captura']}) ====")
            print(json.dumps(doc, indent=2, ensure_ascii=False))

    datos_meteosource = read_data(METEOSOURCE)
    print(f"======== DOCUMENTOS EN 'METEOSOURCE': {len(datos_meteosource)} ========")
    if len(datos_meteosource) > 0:
        for i, doc in enumerate(datos_meteosource):
            print(f"==== DOCUMENTO {i+1} ({doc['timestamp_captura']}) ====")
            print(json.dumps(doc, indent=2, ensure_ascii=False))


def insert_data(collection_name: str, data: dict):
    """
    Inserta un documento en una colección dada.
    Retorna el ID del documento insertado.
    """
    try:
        collection = db[collection_name]
        resultado = collection.insert_one(data)
        print(
            f"Documento insertado en '{collection_name}' con ID: {resultado.inserted_id}"
        )
        return resultado.inserted_id
    except Exception as e:
        print(f"Error insertando documento en MongoDB: {e}")
        return None


if __name__ == "__main__":
    test_connection()
    leer_todo()
