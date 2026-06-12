import requests
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

# Headers
headers = {"X-Auth-Token": API_KEY}

# ============================================
# TEIL 1: Teams holen
# ============================================
print("=" * 60)
print("🏆 TEIL 1: Champions League Teams")
print("=" * 60)

url_teams = "https://api.football-data.org/v4/competitions/CL/teams"
response = requests.get(url_teams, headers=headers)

if response.status_code == 200:
    teams_data = response.json()
    teams = teams_data["teams"]
    print(f"✅ {len(teams)} Teams gefunden")
else:
    print(f"❌ Fehler bei Teams: {response.text}")
    teams = []

# ============================================
# TEIL 2: Spiele holen
# ============================================
print("\n" + "=" * 60)
print("⚽ TEIL 2: Champions League Spiele")
print("=" * 60)

url_matches = "https://api.football-data.org/v4/competitions/CL/matches"
response = requests.get(url_matches, headers=headers)

if response.status_code == 200:
    matches_data = response.json()
    matches = matches_data["matches"]
    print(f"✅ {len(matches)} Spiele gefunden")
    
    # Erste 3 Spiele anzeigen
    print("\n📅 Die ersten 3 Spiele:")
    for match in matches[:3]:
        heim = match["homeTeam"]["shortName"]
        gast = match["awayTeam"]["shortName"]
        datum = match["utcDate"][:10]
        status = match["status"]
        
        if status == "FINISHED":
            tore_heim = match["score"]["fullTime"]["home"]
            tore_gast = match["score"]["fullTime"]["away"]
            ergebnis = f"{tore_heim}:{tore_gast}"
        else:
            ergebnis = "noch nicht gespielt"
        
        print(f"  • {datum}: {heim} vs {gast} ({ergebnis})")
else:
    print(f"❌ Fehler bei Spielen: {response.text}")
    matches = []

# ============================================
# ZUSAMMENFASSUNG
# ============================================
print("\n" + "=" * 60)
print("📊 ZUSAMMENFASSUNG")
print("=" * 60)
print(f"🏆 Teams: {len(teams)}")
print(f"⚽ Spiele: {len(matches)}")

# ============================================
# TEIL 3: In Pandas DataFrame umwandeln!
# ============================================
import pandas as pd

print("\n" + "=" * 60)
print("🐼 TEIL 3: Pandas DataFrames")
print("=" * 60)

# --- Teams DataFrame ---
teams_liste = []
for team in teams:
    teams_liste.append({
        "team_id": team["id"],
        "name": team["name"],
        "short_name": team["shortName"],
        "tla": team["tla"],
        "land": team["area"]["name"],
        "gegruendet": team.get("founded"),
        "stadion": team.get("venue")
    })

df_teams = pd.DataFrame(teams_liste)
print(f"\n✅ Teams DataFrame erstellt: {len(df_teams)} Zeilen, {len(df_teams.columns)} Spalten")
print(df_teams.head())

# --- Spiele DataFrame ---
spiele_liste = []
for match in matches:
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

df_spiele = pd.DataFrame(spiele_liste)
print(f"\n✅ Spiele DataFrame erstellt: {len(df_spiele)} Zeilen, {len(df_spiele.columns)} Spalten")
print(df_spiele.head())

# ============================================
# TEIL 4: Erste Analysen mit Pandas!
# ============================================
print("\n" + "=" * 60)
print("📊 TEIL 4: Erste Analysen")
print("=" * 60)

# --- Analyse 1: Wie viele Teams pro Land? ---
print("\n🌍 Top 5 Länder nach Anzahl Teams:")
teams_pro_land = df_teams.groupby("land").size().sort_values(ascending=False).head(5)
print(teams_pro_land)

# --- Analyse 2: Wie viele Spiele wurden gespielt? ---
print("\n⚽ Status der Spiele:")
status_counts = df_spiele["status"].value_counts()
print(status_counts)

# --- Analyse 3: Nur gespielte Spiele für Tor-Analyse ---
df_gespielt = df_spiele[df_spiele["status"] == "FINISHED"].copy()
print(f"\n✅ Anzahl gespielter Spiele: {len(df_gespielt)}")

# --- Analyse 4: Tore pro Spiel ---
df_gespielt["tore_gesamt"] = df_gespielt["tore_heim"] + df_gespielt["tore_gast"]
print(f"\n📈 Durchschnittliche Tore pro Spiel: {df_gespielt['tore_gesamt'].mean():.2f}")
print(f"📈 Maximale Tore in einem Spiel: {df_gespielt['tore_gesamt'].max()}")

# --- Analyse 5: Top 3 torreichste Spiele ---
print("\n🔥 Top 3 torreichste Spiele:")
top_3 = df_gespielt.nlargest(3, "tore_gesamt")[
    ["datum", "heim_team", "tore_heim", "tore_gast", "gast_team", "tore_gesamt"]
]
print(top_3.to_string(index=False))

# ============================================
# TEIL 5: Daten in CSV speichern!
# ============================================
print("\n" + "=" * 60)
print("💾 TEIL 5: Daten in CSV speichern")
print("=" * 60)

# Teams als CSV speichern
df_teams.to_csv("data/teams.csv", index=False)
print(f"✅ Teams gespeichert: data/teams.csv")

# Spiele als CSV speichern  
df_spiele.to_csv("data/spiele.csv", index=False)
print(f"✅ Spiele gespeichert: data/spiele.csv")

print("\n🎉 Alle Daten erfolgreich gespeichert!")
