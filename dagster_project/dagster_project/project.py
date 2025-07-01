from pathlib import Path

from dagster_dbt import DbtProject

dbt_cryptodata_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "dbt_eth_pipeline", "dbt_cryptodata").resolve(),
    target_path=Path(__file__).joinpath("..", "..", "..", "dbt_eth_pipeline", "dbt_cryptodata", "target").resolve())
dbt_cryptodata_project.prepare_if_dev()
