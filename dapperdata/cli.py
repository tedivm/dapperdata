import os
import sys
from typing import Callable, List, Literal

import click
import typer

from .formatters.json import json_formatter
from .formatters.yaml import yaml_formatter

app = typer.Typer()
from .settings import settings

FORMATTER_MAP = {
    "yml": yaml_formatter,
    "yaml": yaml_formatter,
    "json": json_formatter,
}


TYPER_SUCCESS = typer.style("✓", fg=typer.colors.GREEN, bold=True)
TYPER_FAILURE = typer.style("×", fg=typer.colors.RED, bold=True)
TYPER_MODIFIED = typer.style("⛏", fg=typer.colors.YELLOW, bold=True)


def get_formatter(filename) -> Callable[[str], str] | Literal[False]:
    extension = os.path.splitext(filename)[1].lstrip(".")
    if extension in FORMATTER_MAP:
        return FORMATTER_MAP[extension]
    return False


def format_file(file: str, dry_run: bool = True) -> bool:
    formatter = get_formatter(file)
    if not formatter:
        return False

    with open(file, "r+") as fp:
        contents = fp.read()
        formatted = formatter(contents)

        if not dry_run:
            if contents != formatted:
                fp.seek(0)
                fp.write(formatted)
                fp.truncate()

    # Returns true if the file changed.
    return contents != formatted


def format_directory(dirname: str, dry_run: bool = True, excluded_paths: List[str] = []) -> set[str]:
    changed_files = set([])
    for (root, dirs, files) in os.walk(dirname, topdown=True):

        if root.startswith("./"):
            root = root[2:]

        exclude_root = False
        for excluded_path in excluded_paths:
            if root.startswith(excluded_path):
                exclude_root = True
                # Remove directories to prevent them from being crawled.
                for dir in dirs:
                    dirs.remove(dir)

        if exclude_root:
            continue

        for dir in dirs:
            for excluded_path in excluded_paths:
                if dir.strip("/.").startswith(excluded_path):
                    dirs.remove(dir)

        for path in files:
            file_path = f"{root}/{path}"

            if file_path in excluded_paths:
                continue

            if format_file(file_path, dry_run=dry_run):
                changed_files.add(file_path)

    return changed_files


@app.command()
@click.argument("filename", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("-d", "--dry-run", default=True)
def format(filename: str, dry_run: bool = True):
    print(f"Formatting {filename}")
    if format_file(filename, dry_run=dry_run):
        print("Changes detected.")
    else:
        print("No changes detected.")


@app.command()
@click.argument("dirname", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--dry-run", "-d", default=True)
def pretty(dirname: str, dry_run: bool = True):

    if dry_run:
        typer.echo("Dry Run- No changes will be made.")

    changed_files = format_directory(dirname, dry_run, excluded_paths=settings.exclude_paths)

    if len(changed_files):
        if dry_run:
            typer.echo("Changes needed in the following files:")
            for file in changed_files:
                typer.echo(f"{TYPER_FAILURE} {file}")
            sys.exit(1)
        else:
            typer.echo("Changes made to the following files:")
            for file in changed_files:
                typer.echo(f"{TYPER_MODIFIED} {file}")
            typer.echo(f"All files updated {TYPER_SUCCESS}")
            sys.exit(0)
    else:
        typer.echo(f"No changes needed {TYPER_SUCCESS}")
        sys.exit(0)


if __name__ == "__main__":
    app()
