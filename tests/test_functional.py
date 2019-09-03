import dtoolcore

from . import tmp_dataset_fixture  # NOQA


def test_fixture(tmp_dataset_fixture):  # NOQA
    assert isinstance(tmp_dataset_fixture, dtoolcore.DataSet)
    assert len(tmp_dataset_fixture.identifiers) == 4
