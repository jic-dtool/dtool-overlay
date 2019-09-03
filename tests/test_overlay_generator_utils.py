"""Test utils.overlay_from_glob_rule."""

from . import tmp_dataset_fixture  # NOQA


def test_bool_overlay_from_glob_rule(tmp_dataset_fixture):  # NOQA
    from dtool_overlay.utils import (
        bool_overlay_from_glob_rule,
        TransformOverlays,
    )
    glob_rule = "wt/*"
    overlay = bool_overlay_from_glob_rule(
        "is_wt",
        tmp_dataset_fixture,
        glob_rule
    )
    assert isinstance(overlay, TransformOverlays)

    expected = """identifiers,is_wt,relpaths
1f32389b2f38edb965fc856a1bd2d1a08040407a,False,mut/read_1.fq.gz
2d7cfe62dc3d14f7a9407ba334189b68922f0457,True,wt/read_2.fq.gz
eba3ee4e2f41b172d3a84f425664df4f21a60710,False,mut/read_2.fq.gz
f7b8e915f8af6ea3873104c42efd1770f8eb51db,True,wt/read_1.fq.gz"""

    assert expected == overlay.to_csv()