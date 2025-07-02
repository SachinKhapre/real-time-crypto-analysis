"""
To add a daily schedule that materializes your dbt assets, uncomment the following lines.
"""
from dagster_dbt import build_schedule_from_dbt_selection
from dagster import ScheduleDefinition, define_asset_job
from .assets import dbt_cryptodata_dbt_assets

#schedules = [
#     build_schedule_from_dbt_selection(
#         [dbt_cryptodata_dbt_assets],
#         job_name="materialize_dbt_models",
#         cron_schedule="0 0 * * *",
#         dbt_select="fqn:*",
#     ),
#]

# Job to run all dbt assets
run_all_dbt_assets_job = define_asset_job(
    name="run_all_dbt_assets",
    selection="*",
)

dbt_schedules = ScheduleDefinition(
    job=run_all_dbt_assets_job,
    cron_schedule="*/15 * * * *",
    name="run_all_dbt_assets_schedule"
)