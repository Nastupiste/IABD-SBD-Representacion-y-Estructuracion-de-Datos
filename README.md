# SISTEMAS DE BIG DATA

![Banner para el README.md](https://repository-images.githubusercontent.com/588181932/e36ec678-7984-4cdd-8e4c-a3932772ff8e)

> **Profesor:** Alberto Márquez Alarcón - [@amarala931](https://github.com/amarala931).

## 👥 Miembros del Equipo

- Andrés Prado Morgaz - [@andpramor](https://github.com/andpramor).
- Manuel Jesús de la Rosa Cosano - [@Nastupiste](https://github.com/Nastupiste).

---

## 3.1. Representación y Estructura de Datos

### 🎯 Objetivos

En la actividad 3.1, estos son los objetivos:

1. **Extraer** información de la fuente de datos creada anteriormente (MongoDB en nuestro caso) integrándola en un flujo de Python.

2. **Dominar la manipulación de DataFrames con Polars**, aplicando filtros, agregaciones y transformaciones complejas.

3. **Diseñar visualizaciones interactivas avanzadas** que permitan identificar tendencias, patrones y valores atípicos (outliers) en los datos sobre el poder adquisitivo y el empleo.

4. **Mantener el ciclo de vida del software** mediante el uso de forks en Git y GitHub para la colaboración y el control de versiones.

---

### 👣 Pasos

- [ ] Paso 0. Base de datos.
  - [ ] Adaptar el ejercicio a sqlite3, la MongoDB de la actividad 1.7. ya se ha borrado de la capa gratuita de MongoAtlas.
  - [ ] Crear y almacenar nuevo .env.
  - [ ] Poblar la nueva Base de Datos, ¿una sola API?
  - [ ] Añadir a este README las instrucciones para utilizar este proyecto con UV en lugar de pip, como en el 1.7.

- [ ] Paso 1. Conexión.
  - [ ] Establecer la conexión entre el entorno de Python y la base de datos de la Actividad 1.7.
  - [ ] Extraer datos y cargarlos en un objeto de Polars (read_database o conectores específicos).

- [ ] Paso 2. Limpieza y Estructuración con Polars.
  - [ ] Tratamiento de valores nulos o inconsistentes.
  - [ ] Creación de columnas calculadas (ej.: ratio salario/IPC).
  - [ ] Agrupaciones (GroupBy) para segmentar la información (ej.: por provincias).

Al final de este proceso habrá varios dataframes para un análisis o representación.

- [ ] Paso 3. Generación de Dataframes para Informes.
  - [ ] Exportar archivos CSV con el contenido de cada dataframe.

Cada CSV debe tener una finalidad clara, formando la "capa de plata/oro" lista para ser consumida por otras herramientas.

- [ ] Paso 4. Análisis visual con Plotly.
  - [ ] Gráficos de líneas interactivos para ver la evolución temporal.
  - [ ] Scatter plots (diagramas de dispersión) para ver la correlación entre dos variables.
  - [ ] Gráficos facetados (subplots) para comparar distintas regiones o indicadores simultáneamente.

- [ ] Paso 5. Documentación y Sincronización.
  - [ ] Actualizar el repositorio de GitHub, incluyendo el requirements.txt.
  - [ ] Documentar en este README.md las visualizaciones generadas y conclusiones preliminares obtenidas.
