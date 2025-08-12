import requests
from bs4 import BeautifulSoup
from http.client import HTTPConnection

class StudentLogin:

    def __init__(self, base_url, debug=False):

        # Enable debugging for this session (actually all HTTP connections
        # but blah)
        if debug:
            HTTPConnection.debuglevel = 1

        self.base_url = base_url
        self.session = requests.Session()

    def login(self, emoji_code):
        """Log in using an emoji code."""

        # Get base page
        resp = self.session.get(f"{self.base_url}/emoji-pass/")
        resp.raise_for_status()

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

        post_resp = self.session.post(
            f"{self.base_url}/emoji-pass/", **params)
        post_resp.raise_for_status()

    def me(self):
        """Return information about logged in user."""

        resp = self.session.get(f"{self.base_url}/api/me")
        resp.raise_for_status()

        return resp.json()

    def challenge(self, id):
        """Return information on a challenge by ID number."""

        resp = self.session.get(f"{self.base_url}/api/challenge/{id}")
        resp.raise_for_status()

        return resp.json()
