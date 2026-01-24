from dagster import op, job
import subprocess
import sys
import os

@op
def ingest_raw():
    subprocess.check_call([sys.executable, "ingestion/ingest_coingecko_prices.py"])

@op
def run_sqlmesh(context):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sqlmesh_path = os.path.join(repo_root, "sqlmesh")

    def run(cmd, label):
        context.log.info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            context.log.info(result.stdout)
        if result.stderr:
            context.log.error(result.stderr)
        if result.returncode != 0:
            raise Exception(f"{label} failed")

    # Plan + apply (interactive auto-apply)
    run(["sqlmesh", "-p", sqlmesh_path, "plan", "--auto-apply"], "sqlmesh plan")

    # Data quality
    run(["sqlmesh", "-p", sqlmesh_path, "audit"], "sqlmesh audit")

@job
def crypto_mvp_job():
    # Daily pipeline:
    # 1) Ingest raw data into BigQuery (staging)
    # 2) Materialize analytics models with SQLMesh
    # 3) Validate data quality via SQLMesh audits
    ingest_raw()
    run_sqlmesh()
