"""Utility classes and functions for manipulating overlays."""

import json
import fnmatch
import re


EXCLUDED_NAMES = ("identifiers", "relpaths")


def type_value(s):
    if s in ["True", "False"]:
        return s == "True"
    if s == "":
        return None

    # Int
    if re.match(r"^[0-9]*$", s):
        return int(s)

    # Float
    if re.match(r"^[0-9]*\.[0-9]*$", s) and s != ".":
        return float(s)

    return s


def bool_overlay_from_glob_rule(name, dataset, glob_rule):
    """Return TransformOverlays instance."""
    overlays = TransformOverlays()
    overlays.overlay_names.append(name)
    for identifier in sorted(dataset.identifiers):
        props = dataset.item_properties(identifier)
        relpath = props["relpath"]
        value = fnmatch.fnmatch(relpath, glob_rule)

        overlays.identifiers.append(identifier)
        overlays.relpaths.append(relpath)
        overlays.overlays.setdefault(name, []).append(value)

    return overlays


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
        transform_overlays.overlay_names = [k for k in data.keys()
                                            if k not in EXCLUDED_NAMES]
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

    @classmethod
    def from_csv(cls, csv_data):
        """Return TransformOverlays instance from json representation."""
        transform_overlays = cls()

        lines = csv_data.strip().split("\n")
        header = lines[0].strip().split(",")

        transform_overlays.overlay_names = [k for k in header
                                            if k not in EXCLUDED_NAMES]
        for line in lines[1:]:
            values = line.strip().split(",")
            for key, value in zip(header, values):
                value = type_value(value)
                if key == "identifiers":
                    transform_overlays.identifiers.append(value)
                elif key == "relpaths":
                    transform_overlays.relpaths.append(value)
                else:
                    transform_overlays.overlays.setdefault(
                        key, []).append(value)

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

    def to_json(self):
        """Return json representation of TransformOverlays instance."""
        return json.dumps(self.to_dict(), indent=2)

    def to_csv(self):
        """Return csv representation of TransformOverlays instance."""
        csv_lines = []

        header = ["identifiers"]
        header.extend(self.overlay_names)
        header.append("relpaths")
        csv_lines.append(",".join(header))

        for i in range(len(self.identifiers)):
            row = []
            row.append(str(self.identifiers[i]))
            for name in self.overlay_names:
                value = str(self.overlays[name][i])
                row.append(value)
            row.append(str(self.relpaths[i]))
            csv_lines.append(",".join(row))

        return "\n".join(csv_lines)
