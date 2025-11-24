# Proyecto: Obtención y Almacenamiento de Datos Meteorológicos

![Banner para el README.md](assets/banner_readme.jpg)

Este repositorio contiene el proyecto de grupo para la asignatura Sistemas de Big Data. El objetivo principal es diseñar e implementar un sistema automatizado para la recopilación, limpieza y almacenamiento de datos meteorológicos provenientes de diversas fuentes de datos. El fin último es crear un conjunto de datos robusto para un análisis posterior.

> **Profesor:** Alberto Márquez Alarcón - [@amarala931](https://github.com/amarala931).

## 👥 Miembros del Equipo

- Andrés Prado Morgaz - [@andpramor](https://github.com/andpramor).
- Manuel Jesús de la Rosa Cosano - [@Nastupiste](https://github.com/Nastupiste).
- Tatiana López Velázquez - [@Tati314](https://github.com/Tati314).
- Rubén Prieto Jurado - [@RubenPR2024](https://github.com/RubenPR2024).

---

## 🎯 Objetivos del Proyecto

Siguiendo las directrices del proyecto, nuestros objetivos específicos para esta temática son:

1. **Consultar y Seleccionar Fuentes de Datos:** Investigar y comparar múltiples APIs meteorológicas (verificadas y con acceso automatizable) que sean relevantes para nuestro análisis (ej. datos históricos, pronósticos, etc.).
2. **Evaluar Opciones de Almacenamiento:** Valorar diferentes tecnologías de almacenamiento (BBDD SQL, BBDD NoSQL) y seleccionar la más adecuada para datos de series temporales meteorológicas.
3. **Diseñar la Estructura de Almacenamiento:** Definir el esquema de la base de datos que organice la información de manera eficiente, unificada y lista para el análisis.
4. **Automatizar el Proceso:** Desarrollar scripts para la **Extracción** (consultas a las APIs), **Transformación** (limpieza, unificación de formatos, manejo de nulos) y **Carga** (almacenamiento en la BBDD elegida) de los datos.
5. **Colaboración con Git:** Utilizar el flujo de trabajo de Git (branches, commits, pull requests) para gestionar el desarrollo del código de forma colaborativa.

---

## 🌦️ Fuentes de Datos

Para cumplir con el requisito de "uso de diferentes fuentes de datos" y "fuentes de organismos contrastados", utilizaremos las siguientes APIs:

- **[Open-Meteo](https://open-meteo.com/):** Una API abierta, sin necesidad de API key para uso no comercial. Ofrece datos globales y un amplio historial de datos.
- **[Meteosource](https://www.meteosource.com/es/api-climatologica-actual):** Ofrece un plan grautito donde nos permite consultar tanto pronósticos actuales como futuros.

Hemos descartado algunas otras, basando la selección final y el diseño de la extracción en la facilidad de uso, los límites de tasa (rate limiting) y la riqueza de los datos que ofrecen cada una.

---

## 💻 Stack Tecnológico

- **Lenguaje:** Python 3.13
- **Obtención de Datos:**
  - `requests`: Para realizar las consultas a las APIs REST.
- **Limpieza y Transformación:**
  - `pandas`: Para la manipulación, limpieza y unificación de los datos.
- **Almacenamiento:**
  _Alternativas a valorar:_
  - **Opción 1 (Relacional):** PostgreSQL o MySQL (bueno para datos estructurados).
  - **Opción 2 (NoSQL):** MongoDB (flexible para los JSON de las APIs) o InfluxDB (especializada en series temporales).

---

## 📁 Estructura del Repositorio

```bash
├── scripts/ # Scripts para ETL (extracción, transformación, carga)
│ ├── extract_meteo.py # API 1
│ ├── extract_meteosource.py # API 2
│ ├── transform.py
│ └── load.py
├── mongo/ # Configuración de la base de datos
├── .env.example # Plantilla para variables de entorno (API Keys)
├── .gitignore
└── README.md
```

> **Nota:** El directorio `/data/` (o similar) donde se almacenen los datos crudos o procesados se incluirá en el `.gitignore` para no subir los datos al repositorio, únicamente el código fuente.

---

## 🌊 Flujo de Trabajo con Git

Para cumplir con el objetivo de trabajo colaborativo, se seguirá un flujo de trabajo básico con Git:

1. No hacer `commit` directamente a la rama `main` (o `master`).
2. Crear **ramas** (`feature/`, `fix/`) para cada nueva funcionalidad o script (ej. `feature/api-openweather`).
3. Realizar **Pull Requests (PRs)** para integrar los cambios en `main`.
