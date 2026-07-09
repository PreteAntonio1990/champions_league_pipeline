"""
Champions League Data Pipeline
Antonio Prete - Portfolio Projekt
Mit AWS S3 Integration!
"""

import requests
import os
import logging
import pandas as pd
import boto3
from dotenv import load_dotenv

# .env laden
load_dotenv()
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

# Konstanten
BASE_URL = "https://api.football-data.org/v4/competitions/CL"
HEADERS = {"X-Auth-Token": API_KEY}

# AWS S3 Konfiguration
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")


# ============================================================
# LOGGING-KONFIGURATION
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


# ============================================================
# S3 CLIENT
# ============================================================
def get_s3_client():
    """Erstellt einen S3-Client mit AWS Credentials aus .env"""
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=AWS_REGION
    )


# ============================================================
# EXTRACT
# ============================================================
def hole_teams():
    """Holt alle Champions League Teams von der API."""
    logger.info("Starting team extraction from API")
    
    response = requests.get(f"{BASE_URL}/teams", headers=HEADERS)
    
    if response.status_code != 200:
        logger.error(f"API request failed with status {response.status_code}")
        raise Exception(f"API-Fehler: {response.status_code}")
    
    teams_liste = []
    for team in response.json()["teams"]:
        teams_liste.append({
            "team_id": team["id"],
            "name": team["name"],
            "short_name": team["shortName"],
            "tla": team["tla"],
            "land": team["area"]["name"],
            "gegruendet": team.get("founded"),
            "stadion": team.get("venue")
        })
    
    df = pd.DataFrame(teams_liste)
    logger.info(f"Successfully extracted {len(df)} teams")
    
    return df


def hole_spiele():
    """Holt alle Champions League Spiele von der API."""
    logger.info("Starting match extraction from API")
    
    response = requests.get(f"{BASE_URL}/matches", headers=HEADERS)
    
    if response.status_code != 200:
        logger.error(f"API request failed with status {response.status_code}")
        raise Exception(f"API-Fehler: {response.status_code}")
    
    spiele_liste = []
    for match in response.json()["matches"]:
        spiele_liste.append({
            "spiel_id": match["id"],
            "datum": match["utcDate"][:10],
            "status": match["status"],
            "matchday": match["matchday"],
            "heim_team_id": match["homeTeam"]["id"],
            "heim_team": match["homeTeam"]["shortName"],
            "gast_team_id": match["awayTeam"]["id"],
            "gast_team": match["awayTeam"]["shortName"],
            "tore_heim": match["score"]["fullTime"]["home"],
            "tore_gast": match["score"]["fullTime"]["away"]
        })
    
    df = pd.DataFrame(spiele_liste)
    logger.info(f"Successfully extracted {len(df)} matches")
    
    return df


# ============================================================
# TRANSFORM
# ============================================================
def bereinige_teams(df):
    """Bereinigt den Teams-DataFrame."""
    logger.info("Starting team data cleaning")
    
    df_clean = df.copy()
    df_clean["gegruendet"] = df_clean["gegruendet"].fillna(0).astype(int)
    df_clean["stadion"] = df_clean["stadion"].fillna("Unbekannt")
    df_clean.columns = df_clean.columns.str.upper()
    
    if not df_clean["TEAM_ID"].is_unique:
        logger.error("Duplicates found in team_id!")
        raise ValueError("Duplikate in team_id!")
    
    logger.info(f"Teams cleaned successfully: {len(df_clean)} rows")
    return df_clean


def bereinige_spiele(df):
    """Bereinigt den Spiele-DataFrame."""
    logger.info("Starting match data cleaning")
    
    df_clean = df.copy()
    df_clean["datum"] = pd.to_datetime(df_clean["datum"])
    df_clean["matchday"] = df_clean["matchday"].fillna(0).astype(int)
    df_clean["tore_heim"] = df_clean["tore_heim"].fillna(-1).astype(int)
    df_clean["tore_gast"] = df_clean["tore_gast"].fillna(-1).astype(int)
    df_clean.columns = df_clean.columns.str.upper()
    
    if not df_clean["SPIEL_ID"].is_unique:
        logger.error("Duplicates found in spiel_id!")
        raise ValueError("Duplikate in spiel_id!")
    
    logger.info(f"Matches cleaned successfully: {len(df_clean)} rows")
    return df_clean


# ============================================================
# LOAD - LOKAL (CSV)
# ============================================================
def speichere_csv(df, dateiname):
    """Speichert einen DataFrame als CSV in den data-Ordner."""
    pfad = f"data/{dateiname}"
    df.to_csv(pfad, index=False)
    logger.info(f"Saved locally to {pfad} ({len(df)} rows)")


# ============================================================
# LOAD - CLOUD (S3) - NEU!
# ============================================================
def upload_to_s3(local_file, s3_key):
    """Lädt eine Datei zu AWS S3 hoch."""
    s3 = get_s3_client()
    
    try:
        s3.upload_file(local_file, S3_BUCKET, s3_key)
        logger.info(f"Uploaded to S3: s3://{S3_BUCKET}/{s3_key}")
    except Exception as e:
        logger.error(f"S3 upload failed: {e}")
        raise


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Champions League Pipeline starting (with S3!)")
    logger.info("=" * 60)
    
    try:
        # EXTRACT
        logger.info("Phase 1: EXTRACT")
        df_teams_roh = hole_teams()
        df_spiele_roh = hole_spiele()
        
        # TRANSFORM
        logger.info("Phase 2: TRANSFORM")
        df_teams = bereinige_teams(df_teams_roh)
        df_spiele = bereinige_spiele(df_spiele_roh)
        
        # LOAD - LOKAL
        logger.info("Phase 3a: LOAD (Lokal)")
        speichere_csv(df_teams_roh, "teams.csv")
        speichere_csv(df_spiele_roh, "spiele.csv")
        speichere_csv(df_teams, "teams_clean.csv")
        speichere_csv(df_spiele, "spiele_clean.csv")
        
        # LOAD - CLOUD (S3) - NEU!
        logger.info("Phase 3b: LOAD (AWS S3)")
        upload_to_s3("data/teams.csv", "raw/teams.csv")
        upload_to_s3("data/spiele.csv", "raw/spiele.csv")
        upload_to_s3("data/teams_clean.csv", "clean/teams_clean.csv")
        upload_to_s3("data/spiele_clean.csv", "clean/spiele_clean.csv")
        
        # Summary
        logger.info("=" * 60)
        logger.info(f"Pipeline completed: {len(df_teams)} teams, {len(df_spiele)} matches")
        logger.info(f"Files saved locally + uploaded to S3 bucket: {S3_BUCKET}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise