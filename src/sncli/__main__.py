from sncli.cli import app
from sncli.services.twitter import twitter_app

app.add_typer(twitter_app, name="twitter")

if __name__ == "__main__":
    app()
