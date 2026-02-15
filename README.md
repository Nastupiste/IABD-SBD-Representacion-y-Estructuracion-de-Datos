# SISTEMAS DE BIG DATA: Análisis y cuadros de mando

![Banner para el README.md](https://repository-images.githubusercontent.com/588181932/e36ec678-7984-4cdd-8e4c-a3932772ff8e)

> **Profesor:** Alberto Márquez Alarcón - [@amarala931](https://github.com/amarala931).

## 👥 Miembros del Equipo

- Andrés Prado Morgaz - [@andpramor](https://github.com/andpramor).
- Manuel Jesús de la Rosa Cosano - [@Nastupiste](https://github.com/Nastupiste).

---

## 3.1. Representación y Estructura de Datos

### 🎯 Objetivos

En la actividad 3.1, estos son los objetivos:

1. **Extraer** información de la fuente de datos creada anteriormente integrándola en un flujo de Python.

2. **Dominar la manipulación de DataFrames con Polars**, aplicando filtros, agregaciones y transformaciones complejas.

3. **Diseñar visualizaciones interactivas avanzadas** que permitan identificar tendencias, patrones y valores atípicos (outliers) en los datos sobre el poder adquisitivo y el empleo.

4. **Mantener el ciclo de vida del software** mediante el uso de forks en Git y GitHub para la colaboración y el control de versiones.

---

### 👣 Pasos

- [ ] Paso 0. Prerrequisitos: Base de datos.
  - [x] Adaptar el ejercicio a sqlite3 (la MongoDB de la actividad 1.7. ya se ha borrado de la capa gratuita de MongoAtlas).
  - [x] Poblar la nueva Base de Datos.
  - [x] Añadir a este README las instrucciones para instalar las dependencias de este proyecto.
  - [ ] Añadir LAT y LON para más ciudades.

- [x] Paso 1. Conexión.
  - [x] Establecer la conexión entre el entorno de Python y la base de datos.
  - [x] Extraer datos y cargarlos en un objeto de Polars (read_database o conectores específicos).

- [ ] Paso 2. Limpieza y Estructuración con Polars.
  - [ ] Tratamiento de valores nulos o inconsistentes.
  - [ ] Creación de columnas calculadas (ej.: ratio salario/IPC).
  - [ ] Agrupaciones (GroupBy) para segmentar la información (ej.: por provincias).
  - [ ] DUDA: ¿Los datos se duplican al correr varias veces la extracción? Si la api responde las últimas 12 horas, si se ejecuta de nuevo en menos de 12 horas, ¿tendremos dos ID distintos con la misma información?

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

- [ ] Final. Revisar documentación.
  - [ ] README completo.
  - [ ] `requirements.txt` actualizado.
  - [ ] Análisis de los resultados incluido en README.

---

## 🔢 Instalación de dependencias

### Utilizando la herramienta `uv` (como se ha hecho este proyecto)

Tras clonar el repositorio en local, abrimos una terminal en la raíz del proyecto y ejecutamos:

```bash
uv sync
```

Esto genera un entorno virtual en la raíz del proyecto e instala las dependencias listadas en `pyproject.toml`.

### Utilizando pip

Generamos un entorno virtual (`python -m venv <nombre_del_entorno>`), lo activamos con `.\<nombre_del_entorno>\Scripts\activate` (Windows) o `source <nombre_del_entorno>/bin/activate` (MacOS o Linux).

Hecho esto, ejecutamos:

```bash
pip install -r requirements.txt
```

> NOTA: Hemos generado el archivo `requirements.txt` utilizando el comando de uv `uv export --format requirements-txt --no-hashes --no-annotate --no-header --output-file requirements.txt`.

---

## 💻 Ejecución del proyecto

Con las dependencias instaladas y el entorno virtual activado, ejecutamos el archivo `main.py`:

```bash
python .\main.py
```
