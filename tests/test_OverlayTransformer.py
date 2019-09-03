"""Test the OverlayTransfomer helper class."""


def test_OverlayTransformer_json():

    from dtool_overlay.utils import TransformOverlays

    overlays = {
        "identifiers": [1, 2, 3],
        "is_cool": [True, False, True],
        "relpaths": ["bananas.txt", "melon.txt", "mint.txt"]
    }

    assert overlays == TransformOverlays.from_dict(overlays).to_dict()
