from dataclasses import dataclass
import altair as alt
import polars as pl
from datetime import datetime
import xarray as xr
from pathlib import Path
from plan2eplus.results.sql import get_qoi
from plan2eplus.ops.output.interfaces import OutputVariables
from plys.qoi.custom_qois import CustomQOIRegistry, GenericQOI, CustomQOI


@dataclass(frozen=True)
class EpQOI(GenericQOI):
    name: OutputVariables


class QOIRegistry:
    custom = CustomQOIRegistry
    flow_12 = EpQOI(
        "AFN Linkage Node 1 to Node 2 Volume Flow Rate", "net_flow", "m3/s", "Surface"
    )
    flow_21 = EpQOI(
        "AFN Linkage Node 2 to Node 1 Volume Flow Rate", "net_flow", "m3/s", "Surface"
    )

    temp = EpQOI("Zone Mean Air Temperature", "temp", "C", "Zone")
    mix_vol = EpQOI("AFN Zone Mixing Volume", "mix_vol", "m3", "Zone")
    vent_vol = EpQOI("AFN Zone Ventilation Volume", "vent_vol", "m3", "Zone")

    mix_heat_gain = EpQOI(
        "AFN Zone Mixing Sensible Heat Gain Rate",
        "mix_heat_gain",
        "W",
        "Zone",
    )
    vent_heat_gain = EpQOI(
        "AFN Zone Ventilation Sensible Heat Gain Rate",
        "vent_heat_gain",
        "W",
        "Zone",
    )

    mix_heat_loss = EpQOI(
        "AFN Zone Mixing Sensible Heat Loss Rate",
        "mix_heat_loss",
        "W",
        "Zone",
    )
    vent_heat_loss = EpQOI(
        "AFN Zone Ventilation Sensible Heat Loss Rate",
        "vent_heat_loss",
        "W",
        "Zone",
    )
    wind_pressure = EpQOI(
        "AFN Node Wind Pressure",
        "wind_pressure",
        "Pa",
        "System",
    )


QOIType = CustomQOI | EpQOI


@dataclass
class QOIandData:
    qoi: QOIType
    sql_path: Path
    arr: xr.DataArray | None = None
    dataframe: pl.DataFrame | None = None

    @property
    def original_arr(self):
        if isinstance(self.qoi, EpQOI):
            qoi_res = get_qoi(self.qoi.name, self.sql_path)
            # TODO: introduce some leniency for system variables.
            # assert (
            #     qoi_res.space_type == self.qoi.space_type
            # ), f"Expected space type is {qoi_res.space_type}, but plan2eplus space type is {self.qoi.space_type}"
            assert (
                qoi_res.unit == self.qoi.unit
            ), f"Expected unit for {self.qoi.name} is {qoi_res.unit}, but plan2eplus  unit is {self.qoi.unit}"
            return qoi_res.data_arr

        elif isinstance(self.qoi, CustomQOI):
            # TODO: may have a mapping? but can just change the fx attribute.. don't need a mapping..
            assert self.qoi.fx
            return self.qoi.fx(self.sql_path)
        raise ValueError(
            f"Can't compute arr unless type of self.qoi is CompQOI or EpQOI. Instead, type of variable {self.qoi.name} is {type(self.qoi)}"
        )

    def set_array(self, arr: xr.DataArray):
        self.arr = arr

    def set_dataframe(self, df: pl.DataFrame):
        self.dataframe = df


# TODO: put in xarray helpers! or add to this above..


def select_time(arr: xr.DataArray, dt: datetime | list[datetime]):
    assert "datetimes" in arr.dims
    return arr.sel(datetimes=dt)


def convert_xarray_to_polars(data: xr.DataArray | xr.Dataset, name=""):
    if name:
        data.name = name
    return pl.from_pandas(data.to_dataframe(), include_index=True)


# TODO: make functions for calculating combos and add that to QOI regsitry.. , especially frequently used like net flow rate


# TODO: put in own file for altair helpers
class AltairRenderers:
    BROWSER = "browser"

    @classmethod
    def set_renderer(cls):
        alt.renderers.enable(cls.BROWSER)
