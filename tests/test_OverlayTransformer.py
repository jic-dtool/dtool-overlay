"""Test the OverlayTransfomer helper class."""

import json


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
