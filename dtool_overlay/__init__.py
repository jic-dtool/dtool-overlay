"""dtool_overlay package."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("dtool-overlay")
except PackageNotFoundError:
    # Package is not installed.
    __version__ = "unknown"
