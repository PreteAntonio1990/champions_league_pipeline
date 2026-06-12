"""
Champions League Data → Snowflake Loader
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

load_dotenv()


def get_snowflake_engine():
    return create_engine(URL(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role=os.getenv("SNOWFLAKE_ROLE")
    ))


def lade_teams_in_snowflake(engine):
    print("🏆 Lade Teams in Snowflake...")
    df = pd.read_csv("data/teams_clean.csv")
    print(f"📊 {len(df)} Teams gelesen")
    
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE DIM_TEAM"))
        conn.commit()
    
    df.to_sql("dim_team", engine, if_exists="append", index=False)
    print(f"✅ {len(df)} Teams geladen in DIM_TEAM")


def lade_dim_datum(engine, df_spiele):
    print("\n📅 Lade Datum-Dimension...")
    
    df_datum = pd.DataFrame({"DATUM": pd.to_datetime(df_spiele["DATUM"].unique())})
    df_datum["DATUM_ID"] = df_datum["DATUM"].dt.strftime("%Y%m%d").astype(int)
    df_datum["JAHR"] = df_datum["DATUM"].dt.year
    df_datum["MONAT"] = df_datum["DATUM"].dt.month
    df_datum["TAG"] = df_datum["DATUM"].dt.day
    df_datum["WOCHENTAG"] = df_datum["DATUM"].dt.day_name()
    df_datum["MONAT_NAME"] = df_datum["DATUM"].dt.month_name()
    df_datum = df_datum[["DATUM_ID", "DATUM", "JAHR", "MONAT", "TAG", "WOCHENTAG", "MONAT_NAME"]]
    
    print(f"📊 {len(df_datum)} eindeutige Datums gefunden")
    
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE DIM_DATUM"))
        conn.commit()
    
    df_datum.to_sql("dim_datum", engine, if_exists="append", index=False)
    print(f"✅ {len(df_datum)} Datums geladen in DIM_DATUM")
    return df_datum


def lade_fact_spiel(engine, df_spiele, df_datum):
    print("\n⚽ Lade Spiele in FACT_SPIEL...")
    
    df = df_spiele.copy()
    df["DATUM"] = pd.to_datetime(df["DATUM"])
    df["DATUM_ID"] = df["DATUM"].dt.strftime("%Y%m%d").astype(int)
    df["TORE_GESAMT"] = df["TORE_HEIM"] + df["TORE_GAST"]
    
    df_fact = df[[
        "SPIEL_ID", "DATUM_ID", "HEIM_TEAM_ID", "GAST_TEAM_ID",
        "STATUS", "MATCHDAY", "TORE_HEIM", "TORE_GAST", "TORE_GESAMT"
    ]]
    
    print(f"📊 {len(df_fact)} Spiele vorbereitet")
    
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE FACT_SPIEL"))
        conn.commit()
    
    df_fact.to_sql("fact_spiel", engine, if_exists="append", index=False)
    print(f"✅ {len(df_fact)} Spiele geladen in FACT_SPIEL")


if __name__ == "__main__":
    print("=" * 60)
    print("❄️  Snowflake Loader - Champions League")
    print("=" * 60)
    
    engine = get_snowflake_engine()
    print("🔌 Snowflake-Engine erstellt")
    
    lade_teams_in_snowflake(engine)
    
    df_spiele = pd.read_csv("data/spiele_clean.csv")
    df_datum = lade_dim_datum(engine, df_spiele)
    lade_fact_spiel(engine, df_spiele, df_datum)
    
    engine.dispose()
    
    print("\n" + "=" * 60)
    print("🎉 ALLE DATEN ERFOLGREICH IN SNOWFLAKE!")
    print("=" * 60)
