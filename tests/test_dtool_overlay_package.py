"""Test the dtool_overlay package."""


def test_version_is_string():
    import dtool_overlay
    assert isinstance(dtool_overlay.__version__, str)
