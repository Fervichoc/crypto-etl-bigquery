import os
from google.cloud import bigquery
from dotenv import load_dotenv
from pathlib import Path

# Cargar .env desde la raíz del repo
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET")
LOCATION = os.getenv("BQ_LOCATION", "EU")

def main():
    client = bigquery.Client(project=PROJECT_ID)

    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    dataset_ref.location = LOCATION

    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset already exists: {PROJECT_ID}.{DATASET_ID}")
    except Exception:
        dataset = client.create_dataset(dataset_ref)
        print(f"Created dataset: {dataset.full_dataset_id}")

if __name__ == "__main__":
    main()

print("Bootstrap finished")
