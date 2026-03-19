from pathlib import Path
from cyclopts import App, Parameter
from loguru import logger

from plyze.qoi.data.data import TimeSelection
from plyze.temporal.main import get_temporal_qois
from typing import Annotated

temporal = App("temporal")


@temporal.command()
def study_time_select(ts: TimeSelection):
    logger.debug(ts)


@temporal.command()
def create(
    case_names: Annotated[list[str], Parameter(consume_multiple=True)],
    sqls: Annotated[list[Path], Parameter(consume_multiple=True)],
    ts: TimeSelection,
    outpath: Path,
):
    df = get_temporal_qois(case_names, sqls, ts)
    df.write_csv(outpath)
    logger.success("Finished creating dataframe for temporal data")
