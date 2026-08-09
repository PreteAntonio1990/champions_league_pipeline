# ⚽ Champions League Data Pipeline

End-to-End Cloud-Native ETL Pipeline für UEFA Champions League Daten mit Snowflake Star Schema, AWS S3 und Apache Airflow Orchestrierung.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Pandas](https://img.shields.io/badge/Pandas-2.0-green) ![AWS](https://img.shields.io/badge/AWS-S3-orange) ![Snowflake](https://img.shields.io/badge/Snowflake-Cloud-lightblue) ![Airflow](https://img.shields.io/badge/Airflow-2.8-red) ![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## 👤 Über den Autor

Ich bin Antonio Prete, Quereinsteiger ins Data Engineering nach 11 Jahren Berufserfahrung als Verfahrensmechaniker in der industriellen Produktion. Dieses Projekt entstand als Portfolio-Arbeit während meiner autodidaktischen Weiterbildung. Es zeigt eine typische End-to-End Data Engineering Aufgabe mit modernem Tech-Stack.

## 📋 Über das Projekt

Diese Pipeline holt UEFA Champions League Daten von der Football-Data API, bereinigt sie mit Pandas und speichert sie in mehreren Storage-Layern: lokales CSV, **AWS S3 Cloud-Storage** (Bronze/Silver Pattern) und **Snowflake Star Schema** (Gold Layer). Die Pipeline wurde für tägliche automatische Ausführung mit **Apache Airflow** konzipiert und lief mehrfach erfolgreich durch.

**Was wird verarbeitet:**
- 🏆 36 Champions League Teams
- ⚽ 189+ Spiele der aktuellen Saison
- 📅 Datum-Dimension für Zeit-Analysen

## 🏗️ Architektur

Football-Data API → Python/Pandas (Extract + Transform) → Multiple Storage Layers:s

- **Lokal (CSV):** Für Development und Debugging
- **AWS S3 Bronze:** Raw-Daten in `s3://bucket/raw/`
- **AWS S3 Silver:** Bereinigte Daten in `s3://bucket/clean/`
- **Snowflake (Gold):** Star Schema mit DIM_TEAM, DIM_DATUM, FACT_SPIEL

Orchestriert durch Apache Airflow mit täglichem Schedule und automatischen Retries.

## 📸 Screenshot

### Erfolgreicher Pipeline-Lauf in Apache Airflow

![Erfolgreicher DAG-Lauf](screenshots/airflow_successful_run.png)

Die Pipeline wurde in Apache Airflow orchestriert und lief mehrfach erfolgreich durch. Der Screenshot zeigt einen erfolgreichen Lauf mit Status Success und einer Laufzeit von 11 Sekunden.

## 🛠️ Tech Stack

- **Python 3.12** - Hauptsprache
- **Pandas** - Datenbereinigung und Transformation
- **Requests** - REST API Calls
- **AWS S3** - Cloud Object Storage (boto3)
- **Snowflake** - Cloud Data Warehouse
- **Apache Airflow 2.8** - Workflow Orchestrierung
- **Docker Compose** - Container-Setup
- **SQLAlchemy** - DB-Connection
- **python-dotenv** - Secrets Management
- **Python logging** - Strukturierte Logs

## 📁 Projekt-Struktur
```
champions_league_pipeline/
├── src/
│   ├── extract_data.py       # API-Abruf
│   ├── pipeline.py            # Haupt-ETL Script mit S3-Upload
│   └── load_to_snowflake.py  # Snowflake Loader
├── dags/
│   └── champions_league_dag.py  # Airflow DAG
├── tests/
│   ├── test_api.py            # API-Verbindungstest
│   ├── test_s3.py             # S3-Verbindungstest
│   ├── test_snowflake.py      # Snowflake-Verbindungstest
│   └── upload_test.py         # S3-Upload-Test
├── data/
│   ├── bronze/                # Raw CSV-Dateien
│   ├── silver/                # Bereinigte CSV-Dateien
│   └── gold/                  # Final CSV-Dateien
├── .env                       # API-Keys + AWS-Credentials (nicht in Git!)
├── .gitignore
├── README.md
└── requirements.txt
```
## 🚀 Setup-Anleitung

### Voraussetzungen

- Python 3.12+
- Docker Desktop
- Snowflake Account
- AWS Account mit S3 Bucket
- Football-Data API Key (kostenlos auf football-data.org)

### Installation

1. Repository klonen: `git clone https://github.com/PreteAntonio1990/champions_league_pipeline.git`
2. Python-Pakete installieren: `pip install -r requirements.txt`
3. .env Datei erstellen mit allen Credentials:
   - FOOTBALL_DATA_API_KEY
   - SNOWFLAKE_* Credentials
   - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
   - AWS_REGION, S3_BUCKET_NAME
4. AWS S3 Bucket erstellen (Region: eu-central-1)
5. Snowflake-Tabellen erstellen (Star Schema)
6. Pipeline starten: `python src/pipeline.py`
7. Mit Airflow automatisieren: `docker compose up -d` Web-UI auf http://localhost:8080

## 🌐 AWS S3 Bucket-Struktur
```
s3://champions-league-data-antonio/
├── raw/ (Bronze Layer - Rohdaten)
│   ├── teams.csv
│   └── spiele.csv
└── clean/ (Silver Layer - bereinigt)
├── teams_clean.csv
└── spiele_clean.csv
```
## 📊 Beispiel-Analyse

Top 5 torreichste Spiele mit Star Schema JOIN:

```sql
SELECT d.DATUM, t1.NAME AS HEIM, f.TORE_HEIM, f.TORE_GAST, t2.NAME AS GAST, f.TORE_GESAMT
FROM FACT_SPIEL f
JOIN DIM_DATUM d ON f.DATUM_ID = d.DATUM_ID
JOIN DIM_TEAM t1 ON f.HEIM_TEAM_ID = t1.TEAM_ID
JOIN DIM_TEAM t2 ON f.GAST_TEAM_ID = t2.TEAM_ID
ORDER BY f.TORE_GESAMT DESC LIMIT 5;
```

## 💡 Was ich gelernt habe

- REST APIs mit Authentifizierung und Error-Handling
- Datenbereinigung mit Pandas (dtype-Konvertierung, NULL-Handling)
- Star Schema Data Modeling für analytische Workloads
- **Cloud-Native Architektur mit AWS S3 (Medallion Pattern)**
- **Identity & Access Management (IAM) mit AWS**
- Snowflake Cloud Data Warehouse + RBAC
- Apache Airflow Orchestrierung mit DAGs
- Docker und Container-Setup
- SQLAlchemy mit Transactions
- Idempotenz durch TRUNCATE-INSERT
- Secrets Management mit .env
- **Production-Standard Logging mit Python logging-Modul**

## 🚧 Was ich als nächstes machen würde

- Snowflake liest direkt aus S3 (externes Stage)
- ELT-Pattern mit dbt für SQL-Transformationen
- Inkrementelle Loads statt FULL REFRESH
- CI/CD mit GitHub Actions
- Data Quality Tests mit Great Expectations
- Monitoring + Alerting (CloudWatch)

## 📞 Kontakt

**Antonio Prete** - Aspiring Data Engineer

- LinkedIn: https://www.linkedin.com/in/antonio-prete
- Email: antonio_prete@icloud.com
- GitHub: @PreteAntonio1990

---

⭐ Wenn dir das Projekt gefällt - lass einen Star da!
