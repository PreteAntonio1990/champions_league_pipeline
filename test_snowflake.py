import os
import snowflake.connector
from dotenv import load_dotenv

# .env laden
load_dotenv()

print("🔌 Verbinde mit Snowflake...")

try:
    # Verbindung herstellen
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )
    print("✅ Verbindung erfolgreich!")
    
    # Cursor erstellen (Werkzeug zum Befehle senden)
    cursor = conn.cursor()
    
    # Test 1: Snowflake-Version
    cursor.execute("SELECT CURRENT_VERSION()")
    version = cursor.fetchone()[0]
    print(f"❄️  Snowflake Version: {version}")
    
    # Test 2: Datenbank-Info
    cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")
    db, schema = cursor.fetchone()
    print(f"📦 Database: {db}")
    print(f"📁 Schema: {schema}")
    
    # Test 3: Tabellen anzeigen
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\n📊 Tabellen im Schema:")
    for table in tables:
        print(f"  • {table[1]}")
    
    # Verbindung schließen
    cursor.close()
    conn.close()
    print("\n✅ Test erfolgreich!")
    
except Exception as e:
    print(f"❌ Fehler: {e}")