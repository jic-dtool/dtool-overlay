"""dtool_config.cli module."""

import dtoolcore
import click

from dtool_cli.cli import dataset_uri_argument

from dtool_overlay.utils import (
    TransformOverlays,
    bool_overlay_from_glob_rule,
    pair_overlay_from_suffix,
    value_overlays_from_parsing,
)


@click.group()
def overlays():
    """Overlays provide per item structural metadata."""


@overlays.command()
@dataset_uri_argument
def show(dataset_uri):
    """Show the overlays as CSV table."""
    ds = dtoolcore.DataSet.from_uri(dataset_uri)
    overlays = TransformOverlays.from_dataset(ds)
    click.secho(overlays.to_csv())


@overlays.group()
def template():
    """Create overlay CSV template.

    Templates can be saved as overlays using the ``dtool overlays write``
    command.
    """


@template.command()
@dataset_uri_argument
@click.argument("overlay_name")
@click.argument("glob_rule")
def glob(dataset_uri, overlay_name, glob_rule):
    """Create template with boolean values based on matching of a glob rule.

    For example, one could create an overlay named "is_csv" using the glob_rule
    "*.csv".

    dtool overlays template glob <DS_URI> is_csv '*.csv'

    Note that the glob_rule needs to be quoted on the command line to avoid the
    shell expanding it.
    """
    ds = dtoolcore.DataSet.from_uri(dataset_uri)
    overlays = bool_overlay_from_glob_rule(overlay_name, ds, glob_rule)
    click.secho(overlays.to_csv())


@template.command()
@dataset_uri_argument
@click.argument("parse_rule")
@click.argument("glob_rule")
def parse(dataset_uri, parse_rule, glob_rule):
    """Create template by parsing relpaths that also match a glob rule.

    For example, consider the relpath structure "repl_1/temp_37.0/tomato.csv"
    one could create overlays named "replicate", "treatment", and plant using
    the command below.

    dtool overlays template parse <DS_URI>  \\
      'repl_{replicate:d}/temp_{treatment:f}/{plant}' \\
      '*.csv'

    Note that the parse_rule and glob_rule need to be quoted on the command
    line to avoid the shell expanding it.

    Note also that the replicate values will be typed as integers and the
    temperature values will be typed as floating point, see
    https://pypi.org/project/parse/ for more details.
    """
    ds = dtoolcore.DataSet.from_uri(dataset_uri)
    overlays = value_overlays_from_parsing(ds, parse_rule, glob_rule)
    click.secho(overlays.to_csv())
