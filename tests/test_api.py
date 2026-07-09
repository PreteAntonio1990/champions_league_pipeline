import requests
import os
from dotenv import load_dotenv

# 1. .env-Datei laden
load_dotenv()

# 2. API-Key aus .env holen
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

# 3. Prüfen ob Key geladen wurde
if API_KEY:
    print(f"✅ API-Key gefunden: {API_KEY[:10]}...")
else:
    print("❌ Kein API-Key gefunden! Prüfe deine .env-Datei!")
    exit()

# 4. Headers für die API
headers = {
    "X-Auth-Token": API_KEY
}

# 5. Champions League URL (CL = Champions League)
url = "https://api.football-data.org/v4/competitions/CL"

# 6. API-Call machen
print("\n🌐 API-Anfrage wird gesendet...")
response = requests.get(url, headers=headers)

# 7. Status prüfen
print(f"📡 Status Code: {response.status_code}")

# 8. Antwort anzeigen
if response.status_code == 200:
    data = response.json()
    print(f"\n🏆 Wettbewerb: {data['name']}")
    print(f"🌍 Region: {data['area']['name']}")
    print(f"📅 Aktuelle Saison: {data['currentSeason']['startDate']} - {data['currentSeason']['endDate']}")
    print("\n✅ API funktioniert PERFEKT!")
else:
    print(f"❌ Fehler: {response.text}")