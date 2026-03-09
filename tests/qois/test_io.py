from pathlib import Path
import polars as pl
import tempfile
from plys.examples.casedata import ex
from plys.qoi.data.outputs import gather_standard_data


def test_gather_standard_data():
    case_name = "example"
    with tempfile.TemporaryDirectory() as td:
        tdir = Path(td)
        zp = tdir / "zonal.parquet"
        sp = tdir / "surface.parquet"
        gather_standard_data(case_name, *ex, zp, sp)
        assert pl.read_parquet_metadata(zp)["case_name"] == case_name
