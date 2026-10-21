Jalankan data lake (Minio/seaweedfs)
minio: localhosy 9001 atau API 9000
seaweedfs : localhost:9333 atau API 8333

tambahkan dan jalankan container jupyter
buka browser localhosy:8888

pastikan data lake dan jupyter di network yang sama
buat file sales.csv

id,store,produk,harga,jumlah
1, s1, p1, 1000, 2
2, s2, p2, 2000, 3
3, s3, p3, 0, 0
4, s2, p3, 1400, 6

simpan ke dalam folder bind mount jupyter

 aggregate data sales_cleanded.csv lalu simpan ke bucket gold dan tampilkan
 id, store, total
 1, s1, 2000
 2, s2, 14000
 4, s2, ...