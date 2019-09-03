"""Test the utils.type_value helper function."""


def test_type_value():
    from dtool_overlay.utils import type_value

    assert type_value("True") is True
    assert type_value("False") is False
    assert type_value("") is None
    assert type_value("4") == 4
    assert type(type_value("4")) is int
    assert type_value("4.") == 4.
    assert type(type_value("4.")) is float
    assert type_value("4.0") == 4.
    assert type(type_value("4.0")) is float
    assert type_value(".1") == 0.1
    assert type(type_value(".1")) is float

    assert type(type_value(".")) is str
    assert type_value(".") == "."
