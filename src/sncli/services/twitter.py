import click


@click.group()
def twitter():
    pass


@twitter.command()
def zone():
    click.echo('This is the zone subcommand of the twitter command')
