"""Command-line interface."""
import click
import cli.app

@cli.command()  # @cli, not @click!
def sync():
    click.echo('Syncing')

@click.command()
@click.version_option()
def main() -> None:
    """Social networks cli."""


if __name__ == "__main__":
    main(prog_name="sncli")  # pragma: no cover
