from soneda.cli import app
from soneda.twitter.app import twitter_app

app.add_typer(twitter_app, name="twitter")

if __name__ == "__main__":
    app()
