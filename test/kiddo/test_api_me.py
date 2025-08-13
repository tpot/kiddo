from functools import partial

import handlers
from kiddo.api import StudentLogin

def test_api_me(httpserver):
    """Test calling /api/me endpoint."""

    # Test values for login machinery
    csrf_token = "dummy_csrf_token"
    emoji_pass = "abcd"
    access_token = "dummy_access_token"

    # Login page mock response
    httpserver.expect_request(
        "/emoji-pass/",
        method="GET",
    ).respond_with_data(
        """
        <input type="hidden" name="csrfmiddlewaretoken" value="dummy_csrf_token">
        """,
    )

    # Post emoji password mock response
    _post_emojipass_handler = partial(
        handlers.post_emojipass_handler,
        csrf_token=csrf_token,
        emoji_pass=emoji_pass,
        access_token=access_token,
    )

    httpserver.expect_request(
        "/emoji-pass/",
        method="POST",
    ).respond_with_handler(_post_emojipass_handler)

    url = httpserver.url_for("/")
    s = StudentLogin(url)
    s.login(emoji_pass)

    # Get /api/me mock response

    user_id = 1234

    httpserver.expect_request(
        "/api/me",
        method="GET",
    ). respond_with_json({"id": user_id})

    result = s.me()
    assert result["id"] == user_id
