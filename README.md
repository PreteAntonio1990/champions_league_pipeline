# ⚽ Champions League Data Pipeline

> End-to-End ETL Pipeline für UEFA Champions League Daten von API bis Snowflake Star Schema mit Apache Airflow Orchestrierung.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?logo=pandas)
![Snowflake](https://img.shields.io/badge/Snowflake-Cloud-blue?logo=snowflake)
![Airflow](https://img.shields.io/badge/Airflow-2.8-red?logo=apache-airflow)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)

## 📋 Über das Projekt

Diese Pipeline holt täglich UEFA Champions League Daten von der Football-Data API, bereinigt sie mit Pandas und lädt sie in ein **Star Schema** in Snowflake. Die gesamte Pipeline wird durch **Apache Airflow** orchestriert und läuft täglich automatisch.

**Was wird verarbeitet:**
- 🏆 36 Champions League Teams
- ⚽ 189+ Spiele der aktuellen Saison
- 📅 Datum-Dimension für Zeit-Analysen

## 🏗️ Architektur

Football-Data API → Python/Pandas → CSV → Snowflake Star Schema (DIM_TEAM, DIM_DATUM, FACT_SPIEL)

Orchestriert durch Apache Airflow mit täglichem Schedule und automatischen Retries.

## 🛠️ Tech Stack

- **Python 3.12** - Hauptsprache
- **Pandas** - Datenbereinigung und Transformation
- **Requests** - REST API Calls
- **Snowflake** - Cloud Data Warehouse
- **Apache Airflow 2.8** - Workflow Orchestrierung
- **Docker Compose** - Container-Setup
- **SQLAlchemy** - DB-Connection
- **python-dotenv** - Secrets Management

## 📁 Projekt-Struktur

champions_league_pipeline/
├── .env (API-Keys, NICHT in Git!)
├── .gitignore
├── README.md
├── requirements.txt
├── pipeline.py (Haupt-ETL Script)
├── load_to_snowflake.py (Snowflake Loader)
├── dags/champions_league_dag.py (Airflow DAG)
└── data/ (CSV-Dateien)

## 🚀 Setup-Anleitung

### Voraussetzungen
- Python 3.12+
- Docker Desktop
- Snowflake Account
- Football-Data API Key (kostenlos auf football-data.org)

### Installation

1. Repository klonen:
git clone https://github.com/PreteAntonio1990/champions_league_pipeline.git

2. Python-Pakete installieren:
pip install -r requirements.txt

3. .env Datei erstellen mit allen Credentials

4. Snowflake-Tabellen erstellen (Star Schema)

5. Pipeline starten:
python pipeline.py
python load_to_snowflake.py

6. Mit Airflow automatisieren:
docker compose up -d
Web-UI auf http://localhost:8080

## 📊 Beispiel-Analyse

Top 5 torreichste Spiele mit Star Schema JOIN:

SELECT d.DATUM, t1.NAME AS HEIM, f.TORE_HEIM, f.TORE_GAST, t2.NAME AS GAST, f.TORE_GESAMT
FROM FACT_SPIEL f
JOIN DIM_DATUM d ON f.DATUM_ID = d.DATUM_ID
JOIN DIM_TEAM t1 ON f.HEIM_TEAM_ID = t1.TEAM_ID
JOIN DIM_TEAM t2 ON f.GAST_TEAM_ID = t2.TEAM_ID
ORDER BY f.TORE_GESAMT DESC LIMIT 5;

## 💡 Was ich gelernt habe

- REST APIs mit Authentifizierung
- Datenbereinigung mit Pandas
- Star Schema Data Modeling
- Snowflake Cloud Data Warehouse
- Apache Airflow Orchestrierung
- Docker und Container
- SQLAlchemy mit Transactions
- Idempotenz durch TRUNCATE-INSERT
- Secrets Management mit .env

## 🚧 Was ich als nächstes machen würde

- Code-Zentralisierung mit src/ Modul
- Logging statt print-Statements
- Datenqualität-Tests mit Great Expectations
- Inkrementelle Loads
- dbt für SQL-Transformationen
- CI/CD mit GitHub Actions

## 📞 Kontakt

**Antonio Prete** - Aspiring Data Engineer

- LinkedIn: [Dein LinkedIn-Link hier]
- Email: antonio_prete@icloud.de
- GitHub: @PreteAntonio1990

---

⭐ Wenn dir das Projekt gefällt - lass einen Star da!