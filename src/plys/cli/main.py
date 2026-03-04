from utils4plans.logconfig import logset
import altair as alt

from cyclopts import App

from plys.fpviz.main import plan_plot
from plys.paths import ProjectPaths
from plys.qoi.plots import (
    corr_plot,
    surface_corr_plot,
    surface_qois,
    to_dataframe_with_spaces,
    zone_qois,
)
from plys.qoi.registry import AltairRenderers, QOIType
from plys.qoi.theme import default_theme
from loguru import logger
from pathlib import Path


app = App()


def keep():
    default_theme()
    logger.debug("")


### ------- BEGIN COMMANDS ----------

### ------ SHOW FLOOR PLAN


@app.command()
def show_plan():
    plan_plot(ProjectPaths.sample_idf)


### ------- SINGLE PLOTS


@app.command()
def plot_vol(qoi: QOIType, idf_path: Path, sql_path: Path):
    qoid = to_dataframe_with_spaces(qoi, idf_path, sql_path)
    chart = corr_plot(qoid)
    chart.show()


@app.command()
def plot_surface(qoi: QOIType, idf_path: Path, sql_path: Path):

    qoid = to_dataframe_with_spaces(qoi, idf_path, sql_path)

    chart = surface_corr_plot(qoid)
    chart.show()


### ------- MULTI PLOTS
@app.command()
def plot_vol_many():
    c = zone_qois(ProjectPaths.sample_idf, ProjectPaths.sample_sql)
    c.show()


@app.command()
def plot_surf_many():
    c = surface_qois(ProjectPaths.sample_idf, ProjectPaths.sample_sql)
    c.show()


### ------- END COMMANDS ---------


def main():
    AltairRenderers.set_renderer()
    alt.theme.enable("default_theme")
    logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()
