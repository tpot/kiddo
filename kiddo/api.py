from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from http.client import HTTPConnection

@dataclass
class HarvestConnectionError(Exception):
    base_url: str
    message: str

@dataclass
class HarvestAPIError(Exception):
    status_code: int
    url: str
    message: str = ""

    def __str__(self) -> str:
        base = f"HTTP {self.status_code} on {self.url}"
        return f"{base}: {self.message}" if self.message else base

class HarvestUnauthorisedError(HarvestAPIError):
    pass

class HarvestNotFoundError(HarvestAPIError):
    pass

def raise_for_status(resp):
    """Raise appropriate Exception subclass for HTTP status 403 or 404."""
    if resp.status_code == 401:
        raise HarvestUnauthorisedError(resp.status_code, resp.url)
    if resp.status_code == 404:
        raise HarvestNotFoundError(resp.status_code, resp.url)
    resp.raise_for_status()

class StudentLogin:

    def __init__(self, base_url, debug=False):

        # Enable debugging for this session (actually all HTTP connections
        # but blah)
        if debug:
            HTTPConnection.debuglevel = 1

        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None

    def login(self, emoji_code):
        """Log in using an emoji code."""

        # Get base page
        resp = None

        try:
            resp = self.session.get(f"{self.base_url}/emoji-pass/")
        except requests.exceptions.ConnectionError as e:
            raise HarvestConnectionError(self.base_url, str(e))

        raise_for_status(resp)

        # Pull out CSRF token
        soup = BeautifulSoup(resp.text, "html.parser")

        input_tag = soup.find("input", {"name": "csrfmiddlewaretoken"})
        csrf_token = input_tag["value"]

        # Do emoji login request
        params = {
            "headers": {
                "Referer": f"{self.base_url}/emoji-pass/",
            },

            "cookies": {
                "csrftoken": csrf_token,
            },

            "data": {
                "csrfmiddlewaretoken": csrf_token,
                "emoji_pass": emoji_code,
            },
        }

        post_resp = None

        try:
            post_resp = self.session.post(
                f"{self.base_url}/emoji-pass/", **params)
        except requests.exceptions.ConnectionError as e:
            raise HarvestConnectionError(self.base_url, str(e))

        raise_for_status(post_resp)

        self.access_token = post_resp.cookies.get("access_token")

    def me(self):
        """Return information about logged in user."""

        resp = None

        try:
            resp = self.session.get(f"{self.base_url}/api/me")
        except requests.exceptions.ConnectionError as e:
            raise HarvestConnectionError(self.base_url, str(e))

        raise_for_status(resp)

        return resp.json()

    def challenge(self, id):
        """Return information on a challenge by ID number."""

        resp = None

        try:
            resp = self.session.get(f"{self.base_url}/api/challenge/{id}")
        except requests.exceptions.ConnectionError as e:
            raise HarvestConnectionError(self.base_url, str(e))

        raise_for_status(resp)

        return resp.json()

    def challenge_progress(self, id, version):
        """Return information on a challenge by ID number."""

        resp = None

        try:
            resp = self.session.get(f"{self.base_url}/api/challenge/{id}/version/{version}/progress")
        except requests.exceptions.ConnectionError as e:
            raise HarvestConnectionError(self.base_url, str(e))

        raise_for_status(resp)

        return resp.json()
