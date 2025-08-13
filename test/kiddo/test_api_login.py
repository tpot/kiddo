import json
from functools import partial

from werkzeug.wrappers import Request, Response
from kiddo.api import StudentLogin

def test_login(httpserver):
    """Test Harvest API student login via emoji password."""

    def login_handler(request: Request, csrf_token: str, emoji_pass: str, access_token: str):
        """Request handler for /emoji-pass endpoint."""

        # Verify Referer header
        if not request.referrer.endswith("/emoji-pass/"):
            return Response(
                json.dumps({ "message": "Bad or missing referrer header" }),
                status=401,
                content_type="application/json",
            )

        # Verify CSRF token in cookie
        if request.cookies.get("csrftoken") != csrf_token:
            return Response(
                json.dumps({ "message": "Invalid or missing csrftoken cookie" }),
                status=401,
                content_type="application/json",
            )

        # Verify csrfmiddlewaretoken in form submission
        if request.form.get("csrfmiddlewaretoken") != csrf_token:
            return Response(
                json.dumps({ "message": "Invalid or missing csrfmiddlwaretoken in form submission" }),
                status=401,
                content_type="application/json",
            )

        # Verify csrfmiddlewaretoken in form submission
        if request.form.get("emoji_pass") != emoji_pass:
            return Response(
                json.dumps({ "message": "Invalid or missing emoji_pass in form submission" }),
                status=401,
                content_type="application/json",
            )

        resp = Response(
            json.dumps({ "message": "Success" }),
            status=200,
            content_type="application/json",
            )

        resp.set_cookie("access_token", access_token)

        return resp

    # Test values for login machinery
    csrf_token = "dummy_csrf_token"
    emoji_pass = "abcd"
    access_token = "dummy_access_token"

    # Login page mock resonse
    httpserver.expect_request(
        "/emoji-pass/",
        method="GET",
    ).respond_with_data(
        f"""
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        """,
    )

    bound_handler = partial(
        login_handler,
        csrf_token=csrf_token,
        emoji_pass=emoji_pass,
        access_token=access_token,
    )

    # Post emoji password mock response
    httpserver.expect_request(
        "/emoji-pass/",
        method="POST",
    ).respond_with_handler(bound_handler)

    url = httpserver.url_for("/")
    s = StudentLogin(url)
    s.login(emoji_pass)
