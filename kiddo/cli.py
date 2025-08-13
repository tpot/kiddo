import json
import click
import sys
from urllib.parse import urlparse

from kiddo.api import StudentLogin, HarvestAPIError, HarvestNotFoundError, HarvestUnauthorisedError

@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Display info on what's happening.")
@click.option("--debug", is_flag=True, help="Display a lot of info on what's happening.")
@click.option("--base-url", envvar=["KIDDO_BASE_URL"], help="Base URL of API server.")
@click.pass_context
def cli(ctx, verbose, debug, base_url):

    # Validate base URL
    if base_url is None:
        click.echo("Must specify a base URL with --base-url or $KIDDO_BASE_URL", err=True)
        sys.exit(1)

    parsed_url = urlparse(base_url)

    if parsed_url.scheme not in ("http", "https"):
        click.echo("Invalid base URL - must be http or https.", err=True)
        sys.exit(1)

    if len(parsed_url.query) > 0:
        click.echo("Invalid base URL - should not contain query params.", err=True)
        sys.exit(1)

    # Create student session
    student = StudentLogin(base_url, debug=debug)

    # Make context for subcommands
    ctx.obj = {
        "verbose": verbose,
        "debug": debug,
        "student": student,
    }

@cli.command()
@click.pass_context
@click.option("--code", "emoji_code", required=True, help="Emoji code in plain text format.")
def emoji_login(ctx, emoji_code):
    """Test a student's login using an emoji code."""

    student = ctx.obj["student"]
    verbose = ctx.obj["verbose"]

    try:
        student.login(emoji_code)
    except HarvestAPIError as err:
        click.echo(f"API error: {err}", err=True)
        sys.exit(1)

    # Get user data
    if verbose:
        click.echo("Getting user data...")

    try:
        user_data = student.me()
    except HarvestUnauthorisedError:
        click.echo("Unauthorised, no such emoji code", err=True)
        sys.exit(1)
    except HarvestAPIError as err:
        click.echo(f"API error: {err}", err=True)
        sys.exit(1)

    if verbose:
        click.echo(json.dumps(user_data, indent=2))
    else:
        click.echo(f"Login OK, user_id={user_data['id']}")

@cli.command()
@click.pass_context
@click.option("--code", "emoji_code", required=True, help="Emoji code in plain text format.")
@click.option("--challenge-id", "-c", required=True, type=int, help="ID number of challenge.")
def get_challenge(ctx, emoji_code, challenge_id):
    """Get info on a challenge."""

    student = ctx.obj["student"]
    verbose = ctx.obj["verbose"]

    if verbose:
        click.echo(f"Getting challenge data for id={challenge_id}")

    try:
        student.login(emoji_code)
    except HarvestAPIError as err:
        click.echo(f"API error: {err}", err=True)
        sys.exit(1)

    try:
        result = student.challenge(challenge_id)
        click.echo(json.dumps(result, indent=2))
    except HarvestNotFoundError:
        click.echo(f"No such challenge ID {challenge_id}", err=True)
        sys.exit(1)
    except HarvestUnauthorisedError:
        click.echo("Unauthorised, no such emoji code", err=True)
        sys.exit(1)
    except HarvestAPIError as err:
        click.echo(f"API error: {err}", err=True)
        sys.exit(1)

@cli.command()
@click.pass_context
@click.option("--code", "emoji_code", required=True, help="Emoji code in plain text format.")
@click.option("--challenge-id", "-c", required=True, type=int, help="ID number of challenge.")
@click.option("--challenge-version", required=True, type=int, help="ID number of challenge.")
def get_challenge_progress(ctx, emoji_code, challenge_id, challenge_version):
    """Get progress for a challenge."""

    student = ctx.obj["student"]
    verbose = ctx.obj["verbose"]

    if verbose:
        click.echo(f"Getting challenge progress data for id={challenge_id}, version={challenge_version}")

    try:
        student.login(emoji_code)
    except HarvestAPIError as err:
        click.echo(f"API error: {err}", err=True)
        sys.exit(1)

    try:
        result = student.challenge_progress(challenge_id, challenge_version)
        click.echo(json.dumps(result, indent=2))
    except HarvestNotFoundError:
        click.echo(f"Progress for challenge {challenge_id}, version {challenge_version} not found", err=True)
        sys.exit(1)
    except HarvestUnauthorisedError:
        click.echo("Unauthorised, no such emoji code", err=True)
        sys.exit(1)
    except HarvestAPIError as err:
        click.echo(f"API error: {err}", err=True)
        sys.exit(1)

# Main function invoked by pip
def main():
   cli()

# Keep around the name == "__main__" check so we can run locally
if __name__ == "__main__":
    main()
