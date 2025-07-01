from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from .project import dbt_cryptodata_project


@dbt_assets(manifest=dbt_cryptodata_project.manifest_path)
def dbt_cryptodata_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    