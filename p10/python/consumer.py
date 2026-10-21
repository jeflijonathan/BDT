import json
import boto3
from confluent_kafka import Consumer

s3 = boto3.client(
    "s3",
    endpoint_url="http://seaweedfs:8333",
    aws_access_key_id="admin",
    aws_secret_access_key="secret",
    region_name="us-east-1",
)
try:
    s3.create_bucket(Bucket="gold")
except Exception:
    pass 

consumer = Consumer({
    "bootstrap.servers": "kafka:9092",
    "group.id": "kasir-konsumen",
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["pesanan"])

total = {}
diproses = 0

# Processing
while True:
    pesan = consumer.poll(1.0)
    if pesan is None or pesan.error():
        continue

    pesanan = json.loads(pesan.value())
    menu = pesanan["menu"]
    total[menu] = total.get(menu, 0) + pesanan["jumlah"]
    diproses += 1
    print("Terima:", pesanan, "-> total sekarang:", total)

    if diproses % 10 == 0:
        # simpan hasil ke SeaweedFS setiap 10 pesanan
        s3.put_object(
            Bucket="gold",
            Key="total_penjualan.json",
            Body=json.dumps(total, indent=2),
        )
        print(">>> Hasil disimpan ke SeaweedFS")