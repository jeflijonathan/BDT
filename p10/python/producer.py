import json
import random
import time

from confluent_kafka import Producer

MENU = ["nasi goreng", "mie ayam", "es teh"]

producer = Producer({"bootstrap.servers": "kafka:9092"})

nomor = 0
while True:
    nomor += 1
    pesanan = {
        "nomor": nomor,
        "menu": random.choice(MENU),
        "jumlah": random.randint(1, 3),
    }
    producer.produce("pesanan", value=json.dumps(pesanan))
    producer.flush()
    print("Kirim:", pesanan)
    time.sleep(1)