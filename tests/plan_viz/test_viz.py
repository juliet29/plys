from plys.fpviz.main import plan_plot
from plys.paths import ProjectPaths


def test_plan_plot():
    plan_plot(ProjectPaths.sample_idf, show=False)
    assert 1
