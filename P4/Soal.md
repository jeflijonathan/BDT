Bronze:
Gold: sudah diintegrasikan
silver:
bucketnya ada bronze, gold, silver
bahasa pemograman python yang terhubung dengan api data lake terhubung dalam arti baca isi data lake. untuk membaca di bucket bronze.

docker build -t datalake-bronze-reader .

docker run --rm `  --network="host"`
-e S3_ENDPOINT="http://localhost:9000" `  -e AWS_ACCESS_KEY_ID="admin"`
-e AWS_SECRET_ACCESS_KEY="secretsecret" `
datalake-bronze-reader

Bersihkan data dari bucket bronze, lalu simpan data yang sudah dibersihkan tersebut ke bucket silver

lakukan aggregate pada data dilver tersebut lalu simpan di bucket gold
