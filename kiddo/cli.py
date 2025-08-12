import json
import click

from kiddo.api import StudentLogin

@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Display info on what's happening")
@click.option("--debug", is_flag=True, help="Display a lot of info on what's happening")
@click.option("--base-url", envvar=["KIDDO_BASE_URL"], help="Base URL of API server")
@click.pass_context
def cli(ctx, verbose, debug, base_url):

    ctx.obj = {
        "verbose": verbose,
        "debug": debug,
        "base_url": base_url,
    }

@cli.command()
@click.pass_context
@click.option("--code", "emoji_code", required=True, help="Emoji code in plain text format")
def emoji_login(ctx, emoji_code):
    """Test a student's login using an emoji code."""

    verbose = ctx.obj["verbose"]
    debug = ctx.obj["debug"]
    base_url = ctx.obj["base_url"]

    # Login
    if verbose:
        click.echo("Logging in...")

    params = {
        "debug": debug
    }

    user = StudentLogin(base_url, **params)
    user.login(emoji_code)

    # Get user data
    if verbose:
        click.echo("Getting user data...")

    user_data = user.me()

    if verbose:
        click.echo(json.dumps(user_data, indent=2))
    else:
        click.echo(f"Login OK, user_id={user_data['id']}")

if __name__ == "__main__":
   cli()
