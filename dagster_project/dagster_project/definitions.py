from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import dbt_cryptodata_dbt_assets
from .project import dbt_cryptodata_project
from .schedules import run_all_dbt_assets_job, dbt_schedules

defs = Definitions(
    assets=[dbt_cryptodata_dbt_assets],
    schedules=[dbt_schedules],
    resources={
        "dbt": DbtCliResource(project_dir=dbt_cryptodata_project),
    },
    jobs=[run_all_dbt_assets_job],
)