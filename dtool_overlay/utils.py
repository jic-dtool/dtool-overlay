"""Utility classes and functions for manipulating overlays."""

import json

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

    @classmethod
    def from_json(cls, json_data):
        """Return TransformOverlays instance from json representation."""
        data = json.loads(json_data)
        return cls.from_dict(data)

    def to_dict(self):
        """Return dict representation of TransformOverlays instance."""
        overlays = {
            "identifiers": self.identifiers,
            "relpaths": self.relpaths,
        }
        for name in self.overlay_names:
            overlays[name] = self.overlays[name]
        return overlays

    def to_json(self):
        """Return json representation of TransformOverlays instance."""
        return json.dumps(self.to_dict(), indent=2)
