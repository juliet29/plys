from pathlib import Path
import polars as pl
from plys.qoi.data.data import to_multi_data
from plys.qoi.data.interfaces import CaseQOIandData
from plys.qoi.registries.main import QOIRegistry as QR


# class StandardData(NamedTuple):
#     zonal: pl.DataFrame
#     surface: pl.DataFrame


def get_zonal_qois(idf: Path, sql: Path):
    qois = [
        QR.temp,
        QR.vent_vol,
        QR.vent_heat_gain,
        QR.vent_heat_loss,
        QR.custom.net_vent_heat_gain,
        QR.mix_vol,
        QR.mix_heat_gain,
        QR.mix_heat_loss,
        QR.custom.net_mix_heat_gain,
        QR.custom.combined_volume,
        # TODO: latent heat gain (which is not even in output variable requests currently), net incoming flow over a zone, net outgoing flow over a zone, combined mixing heat loss and heat gain
    ]
    return to_multi_data(qois, idf, sql)


def get_surface_qois(idf: Path, sql: Path):
    qois = [QR.flow_12, QR.flow_21, QR.custom.net_flow]
    return to_multi_data(qois, idf, sql)


# TODO: environmental qois
#
#
def gather_standard_data(
    case_name: str, idf: Path, sql: Path, zonal: Path, surface: Path
):
    # TODO: wondering if some of this logic should be shared with the cli.. wonder if will have more types of qois that want to get data on ..
    metadata = {
        "case_name": case_name
    }  # NOTE: if gets more complex, can have a pydantic model

    zonal_df = get_zonal_qois(idf, sql)
    surface_df = get_zonal_qois(idf, sql)

    zonal_df.write_parquet(zonal, metadata=metadata)
    surface_df.write_parquet(surface, metadata=metadata)


def consolidate_data(case_datas: list[CaseQOIandData]):
    case_names = [i.case_name for i in case_datas]
    # assuming these are of all the same "type" of dataframe, ie zonal qois, or surface_qois, etc..
    df = pl.concat([i.dataframe for i in case_datas]).with_columns(case_name=case_names)
    # NOTE: environmental qois would only need to be recorded once, and can actually be taken directly from the EPW, which is a different process
    return df
