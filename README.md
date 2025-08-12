# Kiddo

Command line tool to interact with the ELSA F-2 Harvest API.

```
Usage: kiddo [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose    Display info on what's happening.
  --debug          Display a lot of info on what's happening.
  --base-url TEXT  Base URL of API server.
  --help           Show this message and exit.

Commands:
  emoji-login  Test a student's login using an emoji code.

```

## Installation

If using regular Python `pip`, install like:
```
$ pip install git+https://github.com/tpot/kiddo.git
```

With `uv`, no installation is required and you can just run like:
```
$ uvx --from git+https://github.com/tpot/kiddo.git kiddo
```

For both methods you can pin to a particular version number by appending a version string to the git URL, e.g `@1.0.0`.

## Usage

You must set the base URL of the API serve, either with the `--api-url` option, or by setting the `KIDDO_BASE_URL` environment variable.
