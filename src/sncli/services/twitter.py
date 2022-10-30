import click
import os


@click.group()
def twitter():
    pass


@twitter.command()
@click.option("--access-token-key", type=str, help="API key", default=lambda: os.environ.get("TWITTER_API_KEY", ""))
@click.option("--api-secret-key", type=str, help="API secret key", default=lambda: os.environ.get("TWITTER_API_SECRET_KEY", ""))
@click.option("--bearer-token", type=str, help="Bearer token", default=lambda: os.environ.get("TWITTER_BEARER_TOKEN", ""))
@click.option("--access-token", type=str, help="Access token", default=lambda: os.environ.get("TWITTER_ACCESS_TOKEN", ""))
@click.option("--access-token-secret", type=str, help="Access token secret", default=lambda: os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", ""))
def configure():
    click.echo("Configuring the Twitter account")
    dot_twitter = os.system("echo $HOME")+".twitter"
    if not os.path.exists(dot_twitter):
        os.system("mkdir -p ~/.sncli")
        f = open(dot_twitter, "wt")
        f.write(f"access_token_key={access_token_key}")
        f.close()
        
