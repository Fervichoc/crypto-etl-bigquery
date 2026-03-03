from dagster import Definitions
from dagster_job import crypto_mvp_job
from .schedules import daily_crypto_mvp_schedule

defs = Definitions(
    jobs=[crypto_mvp_job],
    schedules=[daily_crypto_mvp_schedule],
)