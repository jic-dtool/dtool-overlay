"""Test the dtool overlays command line interface."""

import dtoolcore
from click.testing import CliRunner

from . import tmp_dataset_fixture  # NOQA

FASTQ = ["mut/read_1.fq.gz", "mut/read_2.fq.gz",
         "wt/read_1.fq.gz", "wt/read_2.fq.gz"]


def run(*args, input=None):
    """Invoke ``dtool overlays`` with ``args``; return its output."""
    from dtool_overlay.cli import overlays

    result = CliRunner().invoke(overlays, [str(a) for a in args],
                                input=input)
    assert result.exit_code == 0, result.output
    return result.output


def by_relpath(csv_output, name):
    """Return {relpath: value} of overlay ``name`` in CSV output."""
    from dtool_overlay.utils import TransformOverlays

    overlays = TransformOverlays.from_csv(csv_output)
    return dict(zip(overlays.relpaths, overlays.overlays[name]))


def identifier(relpath):
    return dtoolcore.utils.generate_identifier(relpath)


def test_show_without_overlays(tmp_dataset_fixture):  # NOQA
    output = run("show", tmp_dataset_fixture.uri)
    assert output.splitlines()[0] == "identifiers,relpaths"
    assert sorted(line.split(",")[1] for line in output.splitlines()[1:]
                  if line) == sorted(FASTQ + ["md5.txt"])


def test_template_glob(tmp_dataset_fixture):  # NOQA
    output = run("template", "glob", tmp_dataset_fixture.uri,
                 "is_fastq", "*.fq.gz")
    values = by_relpath(output, "is_fastq")
    assert values == {**{r: True for r in FASTQ}, "md5.txt": False}


def test_template_parse(tmp_dataset_fixture):  # NOQA
    output = run("template", "parse", tmp_dataset_fixture.uri,
                 "{strain}/read_{read:d}.fq.gz")
    assert by_relpath(output, "strain") == {
        "mut/read_1.fq.gz": "mut", "mut/read_2.fq.gz": "mut",
        "wt/read_1.fq.gz": "wt", "wt/read_2.fq.gz": "wt",
        "md5.txt": None}
    assert by_relpath(output, "read") == {
        "mut/read_1.fq.gz": 1, "mut/read_2.fq.gz": 2,
        "wt/read_1.fq.gz": 1, "wt/read_2.fq.gz": 2,
        "md5.txt": None}


def test_template_pairs(tmp_dataset_fixture):  # NOQA
    ds = tmp_dataset_fixture
    expected = {
        "mut/read_1.fq.gz": identifier("mut/read_2.fq.gz"),
        "mut/read_2.fq.gz": identifier("mut/read_1.fq.gz"),
        "wt/read_1.fq.gz": identifier("wt/read_2.fq.gz"),
        "wt/read_2.fq.gz": identifier("wt/read_1.fq.gz"),
        "md5.txt": None,
    }

    output = run("template", "pairs", ds.uri, ".fq.gz")
    assert by_relpath(output, "pair_id") == expected

    output = run("template", "pairs", ds.uri, ".fq.gz", "-n", "mate")
    assert by_relpath(output, "mate") == expected


def test_write_from_file_and_show(tmp_dataset_fixture, tmp_path):  # NOQA
    ds = tmp_dataset_fixture
    template = tmp_path / "template.csv"
    template.write_text(
        run("template", "glob", ds.uri, "is_fastq", "*.fq.gz"))

    run("write", ds.uri, template)

    ds = dtoolcore.DataSet.from_uri(ds.uri)
    assert "is_fastq" in ds.list_overlay_names()
    is_fastq = ds.get_overlay("is_fastq")
    assert is_fastq[identifier("wt/read_1.fq.gz")] is True
    assert is_fastq[identifier("md5.txt")] is False

    assert by_relpath(run("show", ds.uri), "is_fastq") == {
        **{r: True for r in FASTQ}, "md5.txt": False}


def test_write_from_stdin(tmp_dataset_fixture):  # NOQA
    ds = tmp_dataset_fixture
    template = run("template", "parse", ds.uri,
                   "{strain}/read_{read:d}.fq.gz")

    run("write", ds.uri, "-", input=template)

    ds = dtoolcore.DataSet.from_uri(ds.uri)
    assert {"strain", "read"} <= set(ds.list_overlay_names())
    assert ds.get_overlay("read")[identifier("mut/read_2.fq.gz")] == 2
    # Items that do not match the rule are written as "None" in the
    # template and must be stored as null, not as the string "None".
    assert ds.get_overlay("strain")[identifier("md5.txt")] is None
