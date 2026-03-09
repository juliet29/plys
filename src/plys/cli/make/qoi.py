from pathlib import Path

from loguru import logger

from plys.qoi.data.interfaces import CaseQOIandData
from plys.qoi.data.outputs import consolidate_data, gather_standard_data
from cyclopts import App


qoi = App(name="qoi")


@qoi.command()
def create(
    case_name: str, idf_path: Path, sql_path: Path, zonal_path: Path, surface_path: Path
):
    gather_standard_data(case_name, idf_path, sql_path, zonal_path, surface_path)
    logger.success("Finished writing standard data")


@qoi.command()
def consolidate(in_paths: list[Path], out_path: Path):
    datas = [CaseQOIandData.read(p) for p in in_paths]
    df = consolidate_data(datas)
    df.write_parquet(out_path)
    logger.success("Finished consolidating data")
