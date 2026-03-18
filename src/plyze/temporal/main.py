from pathlib import Path
import polars as pl


from plyze.qoi.data.data import select_custom_times, to_dataframe, TimeSelection
from plyze.qoi.data.interfaces import QOIandData
from plyze.qoi.registries.interfaces import QOIType
from plyze.qoi.registries.main import QOIRegistry as QR
from plyze.qoi.xarray_helpers import find_drn_in_name

# NOTE: this has a different organziation than rest of data, so may belong in JPGNV or a different repo entirely, depending on how extensive it becomes..
#


# NOTE:, for time selectio want ALL the times..


def get_dataframe(qoi: QOIType, sql: Path, time_selection: TimeSelection):
    return to_dataframe(
        select_custom_times(qoidata=QOIandData(qoi, sql), ts=time_selection)
    )


def make_wind_pressure_df(sql: Path, ts: TimeSelection):
    # NOTE: not taking the absolute value here...
    DRN = "direction"
    wp = QR.custom.unique_wind_pressure
    df = get_dataframe(wp, sql, ts).with_columns(
        pl.col("space_names")
        .map_elements(find_drn_in_name, return_dtype=pl.String)
        .alias(DRN)
    )

    df_pivot = df.pivot(on=DRN, index="datetimes", values=wp.nickname)

    df_max = df.group_by("datetimes").agg(
        pl.col(wp.nickname).max().alias(f"max {wp.nickname}"),
        pl.col(DRN).max_by(wp.nickname).alias(f"DRN of max {wp.nickname}"),
    )
    return df_pivot.join(df_max, on="datetimes")


def make_zonal_df(sql: Path, ts: TimeSelection):
    zonal_qois = [QR.temp, QR.vent_vol, QR.mix_vol]
    dfs = [get_dataframe(qoi, sql, ts) for qoi in zonal_qois]
    join_df = pl.concat(dfs, how="align")
    return join_df


def get_temporal_qois(case_names: list[str], sqls: list[Path]):
    # df_wind = make_wind_pressure_df()
    # zonal_qois = [QR.temp, QR.vent_vol, QR.mix_vol]
    enviro_qois = [QR.site.all]


# TODO share the schema of the final df!
