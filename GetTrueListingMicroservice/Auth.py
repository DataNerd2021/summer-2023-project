
from google.cloud import storage

def authenticate_implicit_with_adc(project_id="extended-spark-381216"):
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")