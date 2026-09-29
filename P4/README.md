---
type: "BigData"
collections: "20261"
title: "#3 Data Lake"
createdAt: "2026-08-05T03:29:30.010Z"
lastUpdated: "2026-09-24T07:34:00.873Z"
tags: []
url: "https://app.capacities.io/home/d6a7729f-f994-48d3-8efe-fb26a4f59354"
---

# #3 Data Lake

![image](https://capacities-files.s3.eu-central-1.amazonaws.com/private/91325073-230e-4022-8e4b-b6ee9e73fb42/raw.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIA5VTNRR6EBR56K2NK%2F20260924%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20260924T073118Z&X-Amz-Expires=43200&X-Amz-Signature=9e2d927d14352e456dde4b22e705c329f092f5c81481d940428d58c5a4d9a54a&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
[image - Notes](https://app.capacities.io/e288d27f-67f3-4518-a8cf-7caaffd5e145/91325073-230e-4022-8e4b-b6ee9e73fb42)

# Object Storage

Penyimpanan objek adalah tulang punggung arsitektur Data Lake, berbeda dengan sistem file hierarkis (seperti folder di komputer) atau penyimpanan blok.

- **Struktur Datar (Flat Space):** Objek tidak diletakkan di dalam folder bersarang, melainkan di dalam sebuah wadah datar yang disebut _Bucket_.

- **Komponen Objek:** Setiap objek terdiri dari tiga hal: data itu sendiri, metadata yang dapat dikustomisasi, dan pengenal unik global (ID/URL).

- **Keunggulan Pencarian:** Metadata yang kaya memungkinkan pencarian data semi-terstruktur dan tidak terstruktur (seperti gambar, log, dan teks) menjadi sangat cepat tanpa membebani sistem analitik.

# Decoupled Storage & Compute

Pada era _Data Warehouse_ tradisional, kapasitas penyimpanan (hard drive) dan komputasi (CPU/RAM) tergabung dalam satu mesin fisik yang sama (_tightly coupled_). Data Lake modern memisahkan keduanya.

- **Skalabilitas Independen:** Organisasi dapat menambah kapasitas penyimpanan hingga satuan _Petabyte_ tanpa harus membeli server komputasi yang mahal, atau sebaliknya.

- **Efisiensi Biaya:** Penyimpanan data dilakukan pada infrastruktur komoditas yang murah, sementara daya komputasi (_cluster_ analitik) hanya dinyalakan saat kueri dijalankan.

- **Fleksibilitas Arsitektur:** Satu pusat penyimpanan data (_single source of truth_) dapat diakses oleh berbagai mesin komputasi berbeda (misalnya Spark untuk _machine learning_, dan Presto untuk analitik SQL).

# Schema-on-Read

Paradigma ini merupakan kebalikan dari _Schema-on-Write_ yang digunakan pada _Relational Database Management System_ (RDBMS).

- **Penyimpanan Data Mentah:** Data diserap (_ingested_) ke dalam Data Lake dalam format aslinya tanpa modifikasi, pembersihan, atau validasi struktur kolom.

- **Fleksibilitas Analitik:** Struktur, tipe data, dan aturan logika baru diterapkan secara dinamis (_on-the-fly_) oleh aplikasi pembaca saat data tersebut ditarik untuk dianalisis.

- **Kecepatan Penyerapan:** Waktu untuk memasukkan data menjadi sangat instan karena tidak ada proses transformasi berat di awal (_bottleneck-free_).

# Erasure Coding

Erasure Coding (EC) adalah metode perlindungan data dalam sistem penyimpanan terdistribusi di mana sekumpulan data asli difragmentasi dan didistribusikan melintasi berbagai node atau media penyimpanan. Secara keilmuan, EC memungkinkan pemulihan data asli meskipun terjadi kegagalan pada sejumlah node penyimpan, tanpa memerlukan replikasi penuh (1:1).

Konsep ini bergantung pada dua komponen fundamental:

1. **Data Shards (**$k$**)**: Blok atau fragmen dari data asli. Jika sebuah _file_ berukuran $S$ dibagi menjadi $k$ buah _data shards_, maka setiap _shard_ akan memiliki ukuran $\frac{S}{k}$.

2. **Parity Shards (**$m$**)**: Fragmen redundan yang dihasilkan dari operasi matematis terhadap kumpulan _data shards_. Fragmen ini tidak berisi data asli secara langsung, melainkan informasi aljabar yang digunakan untuk merekonstruksi data yang hilang.

# Labs

praktik data lake dengan MinIO

```shell
services:
  minio:
    image: minio/minio:latest
    container_name: minio
    hostname: minio
    ports:
      - "9000:9000"   # Port API S3
      - "9001:9001"   # Port Web Console
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: secretsecret
    volumes:
      - ./docker_volumes/minio:/data
    command: server /data --console-address ":9001"
    restart: unless-stopped
    networks:
      - docker_network

networks:
  docker_network:
    driver: bridge

```

Praktik Data Lake terdistribusi

- wajib minimal 4 node

- minimal 2 node harus running

```shell
services:
  minio1:
    image: quay.io/minio/minio:latest
    container_name: minio1
    volumes:
      - minio1-data:/data
    ports:
      - "9001:9001" # Akses Console UI untuk MinIO 1
      - "9000:9000" # Akses S3 API Utama
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: secretsecret
    command: server http://minio1/data http://minio2/data http://minio3/data http://minio4/data --console-address ":9001"

  minio2:
    image: quay.io/minio/minio:latest
    container_name: minio2
    volumes:
      - minio2-data:/data
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: secretsecret
    command: server http://minio1/data http://minio2/data http://minio3/data http://minio4/data --console-address ":9001"

  minio3:
    image: quay.io/minio/minio:latest
    container_name: minio3
    volumes:
      - minio3-data:/data
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: secretsecret
    command: server http://minio1/data http://minio2/data http://minio3/data http://minio4/data --console-address ":9001"

  minio4:
    image: quay.io/minio/minio:latest
    container_name: minio4
    volumes:
      - minio4-data:/data
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: secretsecret
    command: server http://minio1/data http://minio2/data http://minio3/data http://minio4/data --console-address ":9001"

volumes:
  minio1-data:
  minio2-data:
  minio3-data:
  minio4-data:

```

- Memeriksa cluster

```shell
docker exec -it minio1 sh -c "mc alias set myminio http://localhost:9000 admin secretsecret && mc admin info myminio"
```

- Upload sebuah file ke bucket

- Periksa direktori penyimpanan di masing-masing node

```shell
docker exec -it minio1 bash
bash-5.1# ls /data/hospital/laporan.pdf/
f8d9fb9a-3148-4003-9153-669b85361654  xl.meta
```

MinIO akan membuat sebuah obect yang namanya sama persis dengan nama file tersebut yaitu `laporan.pdf` tetapi object tersebut bukan file mentah.

- Praktik fault tolerance

| Jumlah Node Mati | Status Akses Data                                  | Penjelasan                                                                                            |
| :--------------- | :------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| **1 Node Mati**  | **Normal** (Read & Write Lancar)                   | Batas toleransi minimal terpenuhi.                                                                    |
| **2 Node Mati**  | **Read Only** (Bisa dibaca, tidak bisa tulis baru) | N/2 node aktif (2 node). Data aman dibaca, tapi quorum tulis (harus > N/2 untuk menulis aman) hilang. |
| **3 Node Mati**  | **Error / Offline**                                | Klaster kehilangan terlalu banyak node, data tidak bisa direkonstruksi.                               |

# References

Serra, J. (2024). Deciphering data architectures. " O'Reilly Media, Inc.".
