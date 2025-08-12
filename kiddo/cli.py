import click
from api import StudentLogin

@click.group()
@click.option("--verbose", "-v", is_flag=True)
@click.option("--debug", is_flag=True)
@click.option("--base-url", envvar=["KIDDO_BASE_URL"])
@click.pass_context
def cli(ctx, verbose, debug, base_url):

    ctx.obj = {
        "verbose": verbose,
        "debug": debug,
        "base_url": base_url,
    }

@cli.command()
@click.pass_context
@click.option("--emoji-code", required=True)
def emoji_login(ctx, emoji_code):

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
        print(user_data)

if __name__ == "__main__":
   cli()
