from plyze.examples.casedata import ex
from plyze.examples.time_selection import EXAMPLE_TIME_SELECTION as ets

from plyze.temporal.main import get_temporal_qois


def test_get_temporal_qois():
    df = get_temporal_qois(["a", "b"], [ex.sql, ex.sql], ets)
    assert df.height == len(ets.hours) * 2
