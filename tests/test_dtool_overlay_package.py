"""Test the dtool_overlay package."""


def test_version_is_string():
    import dtool_overlay
    assert isinstance(dtool_overlay.__version__, str)


def test_version_when_not_installed(monkeypatch):
    import importlib
    import importlib.metadata

    import dtool_overlay

    def not_installed(name):
        raise importlib.metadata.PackageNotFoundError(name)

    monkeypatch.setattr(importlib.metadata, "version", not_installed)
    try:
        importlib.reload(dtool_overlay)
        assert dtool_overlay.__version__ == "unknown"
    finally:
        monkeypatch.undo()
        importlib.reload(dtool_overlay)
    assert dtool_overlay.__version__ != "unknown"
