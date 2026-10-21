# Materi 7 : Data Ingestion
# base ingestion : bisa perjam atau persize
# real-time ingestion : lebih cepat bisa 1 sec
# CDC (Change Data Capture) : bisa batch bisa realtime

# cttn:
# docker compose up -d debezium (karna di depens on nya ada 4 itu di debezium, jadi jalankan ini saja)
atau
# docker compose up -d kafka nifi postgres debezium seaweedfs  
atau 1 1
# docker compose up -d kafka
# docker compose up -d nifi

1. masuk container postgres
<!-- docker exec -it postgres bash -->

2. login ke postgres
psql -U admin -d postgres(ini nm databaseny)

3. Buat tabel pelanggan dummy 
CREATE TABLE public.pelanggan (
    id integer primary key,
    nama varchar(100),
    kota varchar(100)
);
insert into public.pelanggan values (1, 'Andi', 'Palembang');
<!-- versi di postgres -->
<!-- postgres=# create table public.pelanggan( id integer primary key, nama varchar(100), kota varchar(100));
CREATE TABLE
postgres=# insert into public.pelanggan values (1, 'Andi', 'Palembang');
INSERT 0 1
postgres=# SELECT * FROM public.pelanggan; -->

4. buat buckets bronze di seaweedfs di localhost:7777 --> klik buckets --> new folder --> bronze

5. buat connector debezium connector-config.json (sudah ada filenya)

6. submit connector
<!-- curl -i -X POST -H "Content-Type: application/json" --data @connector-config.json http://localhost:8083/connectors -->

7. melihat daftar connector
<!-- curl -i -X GET http://localhost:8083/connectors -->
# Kalo ada lagi buat lagi connectornya, jadi ada banyak cdc nya nanti

8. melihat status connector
<!-- curl -s http://localhost:8083/connectors/postgres-cdc/status | python3 -m json.tool -->

9. melihat daftar topic di kafka
<!-- docker exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list -->

10. buka nifi di https://localhost:8443 --> klik advanced karna https



# source : postgresql
# data lake : seaweedfs
# cdc : debezium = memantau perubahan data source, ada penambahan kah, penghapusan kah, perubahankah
# realtime : kafka = kalo ada perubahan diantara 3 itu, maka kafka akan mengambil/bikin prbhn secara realtime
# flowchart : nifi = mengatur alirannya, orkestrasinya, dia yang ngatur nya