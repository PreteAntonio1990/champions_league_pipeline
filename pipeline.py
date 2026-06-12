"""
Champions League Data Pipeline
Antonio Prete - Portfolio Projekt
"""

import requests
import os
import pandas as pd
from dotenv import load_dotenv

# .env laden
load_dotenv()
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

# Konstanten (statt überall hardcoded)
BASE_URL = "https://api.football-data.org/v4/competitions/CL"
HEADERS = {"X-Auth-Token": API_KEY}


def hole_teams():
    """
    Holt alle Champions League Teams von der API.
    
    Returns:
        pd.DataFrame: DataFrame mit Team-Daten
    """
    print("🌐 Hole Teams...")
    
    response = requests.get(f"{BASE_URL}/teams", headers=HEADERS)
    
    # Validierung
    assert response.status_code == 200, f"API-Fehler: {response.status_code}"
    
    # JSON in DataFrame
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
    print(f"✅ {len(df)} Teams geholt")
    
    return df
def hole_spiele():
    """
    Holt alle Champions League Spiele von der API.
    
    Returns:
        pd.DataFrame: DataFrame mit Spiel-Daten
    """
    print("⚽ Hole Spiele...")
    
    response = requests.get(f"{BASE_URL}/matches", headers=HEADERS)
    
    # Validierung
    assert response.status_code == 200, f"API-Fehler: {response.status_code}"
    
    # JSON in DataFrame
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
    print(f"✅ {len(df)} Spiele geholt")
    
    return df
def speichere_csv(df, dateiname):
    """
    Speichert einen DataFrame als CSV in den data-Ordner.
    
    Args:
        df: Der DataFrame
        dateiname: Name der Datei (z.B. "teams.csv")
    """
    pfad = f"data/{dateiname}"
    df.to_csv(pfad, index=False)
    print(f"💾 Gespeichert: {pfad}")

# Main - hier passiert die Magie!
if __name__ == "__main__":
    print("=" * 60)
    print("🏆 Champions League Pipeline")
    print("=" * 60)
    
    # 1. Teams holen
    df_teams = hole_teams()
    
    # 2. Spiele holen
    df_spiele = hole_spiele()
    
    # 3. Alles speichern
    print("\n💾 Speichere Daten...")
    speichere_csv(df_teams, "teams.csv")
    speichere_csv(df_spiele, "spiele.csv")
    
    # 4. Zusammenfassung
    print("\n" + "=" * 60)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"🏆 Teams: {len(df_teams)}")
    print(f"⚽ Spiele: {len(df_spiele)}")
    print("\n✅ Pipeline erfolgreich!")

def bereinige_teams(df):
    """
    Bereinigt den Teams-DataFrame.
    
    Args:
        df: Roher Teams-DataFrame
    
    Returns:
        pd.DataFrame: Bereinigter DataFrame
    """
    print("🧹 Bereinige Teams...")
    
    # Kopie erstellen (Original nicht ändern!)
    df_clean = df.copy()
    
    # 1. NaN bei gegruendet mit 0 füllen, dann zu Int konvertieren
    df_clean["gegruendet"] = df_clean["gegruendet"].fillna(0).astype(int)
    
    # 2. NaN bei stadion mit "Unbekannt" füllen
    df_clean["stadion"] = df_clean["stadion"].fillna("Unbekannt")
    
    # 3. Spalten in Großbuchstaben (Snowflake Best Practice!)
    df_clean.columns = df_clean.columns.str.upper()
    
    # Validierung
    assert df_clean["TEAM_ID"].is_unique, "Duplikate in team_id!"
    assert df_clean.isnull().sum().sum() == 0, "Noch NULL-Werte da!"
    
    print(f"✅ Teams bereinigt: {len(df_clean)} Zeilen")
    return df_clean

def bereinige_spiele(df):
    """
    Bereinigt den Spiele-DataFrame.
    
    Args:
        df: Roher Spiele-DataFrame
    
    Returns:
        pd.DataFrame: Bereinigter DataFrame
    """
    print("🧹 Bereinige Spiele...")
    
    # Kopie erstellen
    df_clean = df.copy()
    
    # 1. Datum als richtiges Datum (statt String!)
    df_clean["datum"] = pd.to_datetime(df_clean["datum"])
    
    # 2. matchday als Integer
    df_clean["matchday"] = df_clean["matchday"].fillna(0).astype(int)
    
    # 3. Tore als Integer (NaN bei geplanten Spielen → -1 als Marker)
    df_clean["tore_heim"] = df_clean["tore_heim"].fillna(-1).astype(int)
    df_clean["tore_gast"] = df_clean["tore_gast"].fillna(-1).astype(int)
    
    # 4. Spalten in GROSSBUCHSTABEN (Snowflake Best Practice)
    df_clean.columns = df_clean.columns.str.upper()
    
    # Validierung
    assert df_clean["SPIEL_ID"].is_unique, "Duplikate in spiel_id!"
    
    print(f"✅ Spiele bereinigt: {len(df_clean)} Zeilen")
    return df_clean


# Main - hier passiert die Magie!
# Main - hier passiert die Magie!
if __name__ == "__main__":
    print("=" * 60)
    print("🏆 Champions League Pipeline")
    print("=" * 60)
    
    # 1. EXTRACT: Daten holen
    print("\n📥 EXTRACT")
    print("-" * 60)
    df_teams_roh = hole_teams()
    df_spiele_roh = hole_spiele()
    
    # 2. TRANSFORM: Daten bereinigen
    print("\n🔧 TRANSFORM")
    print("-" * 60)
    df_teams = bereinige_teams(df_teams_roh)
    df_spiele = bereinige_spiele(df_spiele_roh)
    
    # 3. LOAD: Speichern
    print("\n💾 LOAD")
    print("-" * 60)
    speichere_csv(df_teams, "teams_clean.csv")
    speichere_csv(df_spiele, "spiele_clean.csv")
    
    # 4. Zusammenfassung
    print("\n" + "=" * 60)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"🏆 Teams: {len(df_teams)}")
    print(f"⚽ Spiele: {len(df_spiele)}")
    print("\n✅ Pipeline erfolgreich!")
    
    # Preview der bereinigten Daten
    print("\n📋 Teams (bereinigt):")
    print(df_teams.head())
    print("\n📋 Spiele (bereinigt):")
    print(df_spiele.head())