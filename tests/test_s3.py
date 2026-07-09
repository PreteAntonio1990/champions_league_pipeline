"""
Test S3-Connection
Antonio Prete
"""

import boto3
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()

# S3-Client erstellen
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# Bucket-Name aus .env
bucket_name = os.getenv('S3_BUCKET_NAME')

print(f"🌐 Teste Verbindung zu Bucket: {bucket_name}")

# Liste alle Buckets
try:
    response = s3.list_buckets()
    print("\n✅ Verbindung erfolgreich!")
    print("\n📦 Deine Buckets:")
    for bucket in response['Buckets']:
        print(f"   - {bucket['Name']}")
except Exception as e:
    print(f"\n❌ FEHLER: {e}")