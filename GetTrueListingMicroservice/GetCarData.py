from google.cloud import bigquery
from google.oauth2.service_account import Credentials

credentials = Credentials.from_service_account_file()
client = bigquery.Client(credentials=credentials)

def get_listing_data(): 
    # Perform a query.
    QUERY = (
        'SELECT * FROM `extended-spark-381216.training_data.clean_training_data`'
        'LIMIT 50')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    data = []
    for row in rows:
        data.append(row)

    return data

if __name__ == '__main__':
    listing_data = get_listing_data()
    for item in listing_data:
        print(item)
