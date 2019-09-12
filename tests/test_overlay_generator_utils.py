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
0109d5c3918c504f12a6270574ddd99aa7907b44,False,md5.txt
1f32389b2f38edb965fc856a1bd2d1a08040407a,False,mut/read_1.fq.gz
eba3ee4e2f41b172d3a84f425664df4f21a60710,False,mut/read_2.fq.gz
f7b8e915f8af6ea3873104c42efd1770f8eb51db,True,wt/read_1.fq.gz
2d7cfe62dc3d14f7a9407ba334189b68922f0457,True,wt/read_2.fq.gz"""

    print(overlay.to_csv())

    assert expected == overlay.to_csv()


def test_pair_overlay_from_suffix(tmp_dataset_fixture):  # NOQA
    from dtool_overlay.utils import (
        pair_overlay_from_suffix,
        TransformOverlays,
    )
    suffix = ".fq.gz"
    overlay = pair_overlay_from_suffix(
        "pair_id",
        tmp_dataset_fixture,
        suffix
    )
    assert isinstance(overlay, TransformOverlays)

    expected = """identifiers,pair_id,relpaths
0109d5c3918c504f12a6270574ddd99aa7907b44,None,md5.txt
1f32389b2f38edb965fc856a1bd2d1a08040407a,eba3ee4e2f41b172d3a84f425664df4f21a60710,mut/read_1.fq.gz
eba3ee4e2f41b172d3a84f425664df4f21a60710,1f32389b2f38edb965fc856a1bd2d1a08040407a,mut/read_2.fq.gz
f7b8e915f8af6ea3873104c42efd1770f8eb51db,2d7cfe62dc3d14f7a9407ba334189b68922f0457,wt/read_1.fq.gz
2d7cfe62dc3d14f7a9407ba334189b68922f0457,f7b8e915f8af6ea3873104c42efd1770f8eb51db,wt/read_2.fq.gz"""  # NOQA

    assert expected == overlay.to_csv()


def test_value_overlays_from_parsing(tmp_dataset_fixture):  # NOQA
    from dtool_overlay.utils import (
        value_overlays_from_parsing,
        TransformOverlays,
    )
    parse_rule = "{line}/read_{read:d}.fq.gz"
    overlays = value_overlays_from_parsing(
        tmp_dataset_fixture,
        parse_rule,
    )
    assert isinstance(overlays, TransformOverlays)

    expected = """identifiers,line,read,relpaths
0109d5c3918c504f12a6270574ddd99aa7907b44,None,None,md5.txt
1f32389b2f38edb965fc856a1bd2d1a08040407a,mut,1,mut/read_1.fq.gz
eba3ee4e2f41b172d3a84f425664df4f21a60710,mut,2,mut/read_2.fq.gz
f7b8e915f8af6ea3873104c42efd1770f8eb51db,wt,1,wt/read_1.fq.gz
2d7cfe62dc3d14f7a9407ba334189b68922f0457,wt,2,wt/read_2.fq.gz"""  # NOQA

    assert expected == overlays.to_csv()

    for value in overlays.overlays["read"]:
        if value is not None:
            assert type(value) is int
