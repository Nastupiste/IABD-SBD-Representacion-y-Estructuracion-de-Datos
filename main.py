def main():
    print(
        "Paso 1: llamar a scripts_3_1/db_connector.py para obtener los datos de MongoDB en un objeto de Polars."
    )

    print(
        "Paso 2: llamar a scripts_3_1/data_processor.py, clean_data() para transformar los datos y obtener un nuevo objeto de Polars."
    )

    print(
        "Paso 3: llamar a scripts_3_1/data_processor.py, create_columns() y structure_data() para crear nuevas columnas calculadas y agrupadas."
    )

    print(
        "Paso 4: llamar a scripts_3_1/visualizer.py para generar gráficos con Plotly."
    )


if __name__ == "__main__":
    main()
