import os
from google.cloud import bigquery
from dotenv import load_dotenv

print(">>> Starting GCP connection test")

load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")
print(f">>> Project ID from env: {project_id}")

client = bigquery.Client(project=project_id)

print(f">>> Connected to project: {project_id}")

datasets = list(client.list_datasets())

print(">>> Datasets found:")
for ds in datasets:
    print("-", ds.dataset_id)
