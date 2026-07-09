"""
S3 Upload Test
Antonio Prete
"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# S3-Client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

bucket_name = os.getenv('S3_BUCKET_NAME')

# Test: Eine CSV hochladen!
local_file = 'data/teams_clean.csv'
s3_key = 'raw/teams_clean.csv'

print(f"📤 Lade hoch: {local_file}")
print(f"   → s3://{bucket_name}/{s3_key}")

try:
    s3.upload_file(local_file, bucket_name, s3_key)
    print("\n✅ Upload erfolgreich!")
    
    # Liste was im Bucket ist
    print("\n📦 Im Bucket:")
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            size_kb = obj['Size'] / 1024
            print(f"   - {obj['Key']} ({size_kb:.1f} KB)")
    else:
        print("   (leer)")
except Exception as e:
    print(f"\n❌ FEHLER: {e}")