"""Utility classes and functions for manipulating overlays."""

EXCLUDED_NAMES = ("identifiers", "relpaths")


class TransformOverlays(object):
    """Convert overlays between csv, dict and dataset representations."""

    def __init__(self):
        self.overlay_names = []
        self.identifiers = []
        self.relpaths = []
        self.overlays = {}

    @classmethod
    def from_dict(cls, data):
        """Return TransformOverlays instance from dict representation."""
        transform_overlays = cls()
        transform_overlays.overlay_names = [k for k in data.keys()]
        transform_overlays.identifiers = data["identifiers"]
        transform_overlays.relpaths = data["relpaths"]
        for name in transform_overlays.overlay_names:
            transform_overlays.overlays[name] = data[name]
        return transform_overlays

    def to_dict(self):
        """Return dict representation of TransformOverlays instance."""
        overlays = {
            "identifiers": self.identifiers,
            "relpaths": self.relpaths,
        }
        for name in self.overlay_names:
            overlays[name] = self.overlays[name]
        return overlays
