import os
import boto3
import json
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=DeprecationWarning)

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:9000")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "admin")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "secretsecret")

BRONZE_BUCKET = "bronze"
SILVER_BUCKET = "silver"
GOLD_BUCKET = "gold"

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

def run_data_lake_pipeline():
    s3_client = get_s3_client()

    try:
        # 1. Pastikan semua bucket (Bronze, Silver, Gold) tersedia
        existing_buckets = [b['Name'] for b in s3_client.list_buckets().get('Buckets', [])]
        for bucket_name in [BRONZE_BUCKET, SILVER_BUCKET, GOLD_BUCKET]:
            if bucket_name not in existing_buckets:
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"[INFO] Bucket '{bucket_name}' berhasil dibuat.")

        # ==========================================
        # TAHAP 1: BRONZE -> SILVER (Cleaning & Flattening)
        # ==========================================
        print("\n==========================================")
        print("MENGANALISIS DAN MEMBERSIHKAN DATA (BRONZE -> SILVER)")
        print("==========================================")
        
        response = s3_client.list_objects_v2(Bucket=BRONZE_BUCKET)
        if 'Contents' not in response:
            print(f"[WARN] Bucket '{BRONZE_BUCKET}' kosong.")
            return

        for obj in response['Contents']:
            file_key = obj['Key']
            if not file_key.endswith('.json'):
                continue
                
            print(f"\n[INFO] Membaca file mentah dari Bronze: {file_key}")
            file_obj = s3_client.get_object(Bucket=BRONZE_BUCKET, Key=file_key)
            raw_data = json.loads(file_obj['Body'].read().decode('utf-8'))

            cleaned_transactions = []
            ingest_time = raw_data.get("ingest_timestamp")
            
            for tx in raw_data.get("payload", []):
                # Bersihkan spasi liar (whitespace stripping)
                full_name = tx["customer"]["full_name"].strip() if tx["customer"].get("full_name") else None
                city = tx["customer"]["city"].strip() if tx["customer"].get("city") else None
                
                # Ubah notes kosong/spasi menjadi None (NULL)
                notes = tx.get("notes", "")
                if notes:
                    notes = notes.strip()
                    if notes == "":
                        notes = None

                cleaned_tx = {
                    "transaction_id": tx.get("transaction_id"),
                    "cust_id": tx["customer"].get("cust_id"),
                    "full_name": full_name,
                    "city": city,
                    "total_paid": tx.get("total_paid"),
                    "status": tx.get("status"),
                    "notes": notes,
                    "ingest_timestamp": ingest_time
                }
                cleaned_transactions.append(cleaned_tx)

            cleaned_json_output = {
                "source_system": raw_data.get("source_system"),
                "batch_id": raw_data.get("batch_id"),
                "cleaned_timestamp": pd.Timestamp.now().isoformat(),
                "payload": cleaned_transactions
            }

            # Simpan ke Bucket Silver
            silver_file_key = f"cleaned_{os.path.splitext(file_key)[0]}.json"
            s3_client.put_object(
                Bucket=SILVER_BUCKET,
                Key=silver_file_key,
                Body=json.dumps(cleaned_json_output, indent=4).encode('utf-8')
            )
            print(f"[SUCCESS] Data bersih disimpan ke '{SILVER_BUCKET}/{silver_file_key}'")

        # ==========================================
        # TAHAP 2: SILVER -> GOLD (Aggregation)
        # ==========================================
        print("\n==========================================")
        print("MELAKUKAN AGREGASI DATA (SILVER -> GOLD)")
        print("==========================================")

        silver_response = s3_client.list_objects_v2(Bucket=SILVER_BUCKET)
        for obj in silver_response.get('Contents', []):
            file_key = obj['Key']
            if not file_key.endswith('.json'):
                continue
                
            print(f"\n[INFO] Membaca data bersih dari Silver: {file_key}")
            file_obj = s3_client.get_object(Bucket=SILVER_BUCKET, Key=file_key)
            silver_data = json.loads(file_obj['Body'].read().decode('utf-8'))

            df = pd.DataFrame(silver_data.get("payload", []))
            if df.empty:
                print("[WARN] DataFrame kosong, lewati agregasi.")
                continue

            # Proses Agregasi (Berdasarkan Kota)
            print("[INFO] Menghitung metrik bisnis per kota...")
            df_agg = df.groupby("city").agg(
                total_transactions=('transaction_id', 'count'),
                total_revenue=('total_paid', 'sum'),
                average_paid=('total_paid', 'mean')
            ).reset_index()

            print("\n--- Hasil Ringkasan (Gold Layer) ---")
            print(df_agg)

            gold_output = {
                "aggregation_level": "by_city",
                "aggregated_timestamp": pd.Timestamp.now().isoformat(),
                "metrics": df_agg.to_dict(orient="records")
            }

            # Simpan ke Bucket Gold
            gold_file_key = "agg_sales_by_city.json"
            s3_client.put_object(
                Bucket=GOLD_BUCKET,
                Key=gold_file_key,
                Body=json.dumps(gold_output, indent=4).encode('utf-8')
            )
            print(f"[SUCCESS] Data agregasi berhasil disimpan ke '{GOLD_BUCKET}/{gold_file_key}'")

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan pada pipeline: {e}")

if __name__ == "__main__":
    run_data_lake_pipeline()