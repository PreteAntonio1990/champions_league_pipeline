"""
Champions League Data Pipeline DAG
Antonio Prete - Portfolio Projekt
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import requests
import pandas as pd

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4/competitions/CL"
HEADERS = {"X-Auth-Token": API_KEY}
DATA_DIR = "/opt/airflow/data"


def extract_data():
    print("🌐 EXTRACT...")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    response = requests.get(f"{BASE_URL}/teams", headers=HEADERS)
    assert response.status_code == 200
    teams_liste = [{
        "team_id": t["id"], "name": t["name"], "short_name": t["shortName"],
        "tla": t["tla"], "land": t["area"]["name"],
        "gegruendet": t.get("founded"), "stadion": t.get("venue")
    } for t in response.json()["teams"]]
    pd.DataFrame(teams_liste).to_csv(f"{DATA_DIR}/teams.csv", index=False)
    print(f"✅ {len(teams_liste)} Teams")
    
    response = requests.get(f"{BASE_URL}/matches", headers=HEADERS)
    assert response.status_code == 200
    spiele_liste = [{
        "spiel_id": m["id"], "datum": m["utcDate"][:10],
        "status": m["status"], "matchday": m["matchday"],
        "heim_team_id": m["homeTeam"]["id"], "heim_team": m["homeTeam"]["shortName"],
        "gast_team_id": m["awayTeam"]["id"], "gast_team": m["awayTeam"]["shortName"],
        "tore_heim": m["score"]["fullTime"]["home"],
        "tore_gast": m["score"]["fullTime"]["away"]
    } for m in response.json()["matches"]]
    pd.DataFrame(spiele_liste).to_csv(f"{DATA_DIR}/spiele.csv", index=False)
    print(f"✅ {len(spiele_liste)} Spiele")


def transform_data():
    print("🧹 TRANSFORM...")
    df_teams = pd.read_csv(f"{DATA_DIR}/teams.csv")
    df_teams["gegruendet"] = df_teams["gegruendet"].fillna(0).astype(int)
    df_teams["stadion"] = df_teams["stadion"].fillna("Unbekannt")
    df_teams.columns = df_teams.columns.str.upper()
    df_teams.to_csv(f"{DATA_DIR}/teams_clean.csv", index=False)
    
    df_spiele = pd.read_csv(f"{DATA_DIR}/spiele.csv")
    df_spiele["datum"] = pd.to_datetime(df_spiele["datum"])
    df_spiele["matchday"] = df_spiele["matchday"].fillna(0).astype(int)
    df_spiele["tore_heim"] = df_spiele["tore_heim"].fillna(-1).astype(int)
    df_spiele["tore_gast"] = df_spiele["tore_gast"].fillna(-1).astype(int)
    df_spiele.columns = df_spiele.columns.str.upper()
    df_spiele.to_csv(f"{DATA_DIR}/spiele_clean.csv", index=False)
    print("✅ Bereinigt")


def load_to_snowflake():
    from sqlalchemy import create_engine, text
    from snowflake.sqlalchemy import URL
    
    print("❄️ LOAD...")
    engine = create_engine(URL(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role=os.getenv("SNOWFLAKE_ROLE")
    ))
    
    # Teams - ohne conn.commit() (alte SQLAlchemy-Version!)
    df_teams = pd.read_csv(f"{DATA_DIR}/teams_clean.csv")
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE DIM_TEAM"))
    df_teams.to_sql("dim_team", engine, if_exists="append", index=False)
    print(f"✅ {len(df_teams)} Teams")
    
    # DIM_DATUM
    df_spiele = pd.read_csv(f"{DATA_DIR}/spiele_clean.csv")
    df_datum = pd.DataFrame({"DATUM": pd.to_datetime(df_spiele["DATUM"].unique())})
    df_datum["DATUM_ID"] = df_datum["DATUM"].dt.strftime("%Y%m%d").astype(int)
    df_datum["JAHR"] = df_datum["DATUM"].dt.year
    df_datum["MONAT"] = df_datum["DATUM"].dt.month
    df_datum["TAG"] = df_datum["DATUM"].dt.day
    df_datum["WOCHENTAG"] = df_datum["DATUM"].dt.day_name()
    df_datum["MONAT_NAME"] = df_datum["DATUM"].dt.month_name()
    df_datum = df_datum[["DATUM_ID", "DATUM", "JAHR", "MONAT", "TAG", "WOCHENTAG", "MONAT_NAME"]]
    
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE DIM_DATUM"))
    df_datum.to_sql("dim_datum", engine, if_exists="append", index=False)
    print(f"✅ {len(df_datum)} Datums")
    
    # FACT_SPIEL
    df = df_spiele.copy()
    df["DATUM"] = pd.to_datetime(df["DATUM"])
    df["DATUM_ID"] = df["DATUM"].dt.strftime("%Y%m%d").astype(int)
    df["TORE_GESAMT"] = df["TORE_HEIM"] + df["TORE_GAST"]
    df_fact = df[["SPIEL_ID", "DATUM_ID", "HEIM_TEAM_ID", "GAST_TEAM_ID",
                  "STATUS", "MATCHDAY", "TORE_HEIM", "TORE_GAST", "TORE_GESAMT"]]
    
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE FACT_SPIEL"))
    df_fact.to_sql("fact_spiel", engine, if_exists="append", index=False)
    print(f"✅ {len(df_fact)} Spiele")
    
    engine.dispose()
    print("🎉 LOAD erfolgreich!")


default_args = {
    "owner": "antonio_prete",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="champions_league_pipeline",
    description="ETL Pipeline für UEFA Champions League",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["champions_league", "etl", "portfolio"],
) as dag:
    
    task_extract = PythonOperator(task_id="extract_data", python_callable=extract_data)
    task_transform = PythonOperator(task_id="transform_data", python_callable=transform_data)
    task_load = PythonOperator(task_id="load_to_snowflake", python_callable=load_to_snowflake)
    
    task_extract >> task_transform >> task_load
