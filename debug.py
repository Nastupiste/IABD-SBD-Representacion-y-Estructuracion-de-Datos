import json
from scripts.mongo_connection import read_data
from scripts.graficas import get_latest_document

if __name__ == "__main__":
    print("OPENMETEO:")
    documentos = read_data("openmeteo")
    latest_document = get_latest_document(documentos)
    print("Último documento:", latest_document.get("timestamp_captura"))
    print("Todos los timestamps de captura:")
    for doc in documentos:
        print(doc.get("timestamp_captura"))
    print(json.dumps(latest_document, indent=2, ensure_ascii=False))

    print("\nMETEOSOURCE:")
    documentos = read_data("meteosource")
    latest_document = get_latest_document(documentos)
    print("Último documento:", latest_document.get("timestamp_captura"))
    print("Todos los timestamps de captura:")
    for doc in documentos:
        print(doc.get("timestamp_captura"))
    print(json.dumps(latest_document, indent=2, ensure_ascii=False))
