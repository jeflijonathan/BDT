import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://seaweedfs:8333",
    aws_access_key_id="admin",
    aws_secret_access_key="secret",
    region_name="us-east-1",
)

file = s3.get_object(Bucket="gold", Key="total_penjualan.json")
print(file["Body"].read().decode())