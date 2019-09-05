"""Test the OverlayTransfomer helper class."""

import json

from . import tmp_dataset_fixture  # NOQA


def test_OverlayTransformer_dict():

    from dtool_overlay.utils import TransformOverlays

    overlays = {
        "identifiers": [1, 2, 3],
        "is_cool": [True, False, True],
        "relpaths": ["bananas.txt", "melon.txt", "mint.txt"]
    }

    assert overlays == TransformOverlays.from_dict(overlays).to_dict()


def test_OverlayTransformer_json():

    from dtool_overlay.utils import TransformOverlays

    overlays = {
        "identifiers": [1, 2, 3],
        "is_cool": [True, False, True],
        "relpaths": ["bananas.txt", "melon.txt", "mint.txt"]
    }

    assert overlays == json.loads(
        TransformOverlays.from_json(
            json.dumps(overlays)
        ).to_json()
    )


def test_OverlayTransformer_csv():

    from dtool_overlay.utils import TransformOverlays

    overlays = {
        "identifiers": [1, 2, 3],
        "is_cool": [True, False, True],
        "relpaths": ["bananas.txt", "melon.txt", "mint.txt"]
    }

    csv = """identifiers,is_cool,relpaths
1,True,bananas.txt
2,False,melon.txt
3,True,mint.txt"""

    assert overlays == TransformOverlays.from_csv(csv).to_dict()
    assert csv == TransformOverlays.from_csv(csv).to_csv()


def test_OverlayTransformet_dataset(tmp_dataset_fixture):  # NOQA
    from dtool_overlay.utils import (
        TransformOverlays,
        value_overlays_from_parsing,
    )

    parse_rule = "{line}/read_{read:d}.fq.gz"
    overlays = value_overlays_from_parsing(
        tmp_dataset_fixture,
        parse_rule,
    )

    expected = """identifiers,line,read,relpaths
0109d5c3918c504f12a6270574ddd99aa7907b44,None,None,md5.txt
1f32389b2f38edb965fc856a1bd2d1a08040407a,mut,1,mut/read_1.fq.gz
2d7cfe62dc3d14f7a9407ba334189b68922f0457,wt,2,wt/read_2.fq.gz
eba3ee4e2f41b172d3a84f425664df4f21a60710,mut,2,mut/read_2.fq.gz
f7b8e915f8af6ea3873104c42efd1770f8eb51db,wt,1,wt/read_1.fq.gz"""  # NOQA

    assert expected == overlays.to_csv()

    assert tmp_dataset_fixture.list_overlay_names() == []

    overlays.put_in_dataset(tmp_dataset_fixture)
    expected_names = set(overlays.overlay_names)
    assert expected_names == set(tmp_dataset_fixture.list_overlay_names())

    overlays_from_dataset = TransformOverlays.from_dataset(tmp_dataset_fixture)
    assert expected == overlays_from_dataset.to_csv()
