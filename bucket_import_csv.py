import boto3

session = boto3.Session()

s3 = session.client('s3', region_name='eu-west-3')

bucket_name = 'bucketminiprojet'
csv_files = ["raw_customers.csv", "raw_items.csv", "raw_orders.csv", "raw_products.csv", "raw_stores.csv", "raw_supplies.csv" ]

s3.create_bucket(Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': 'eu-west-3'  
    })

for file in csv_files:
    s3.upload_file("./docs/"+file, bucket_name, file)
