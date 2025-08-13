from werkzeug.wrappers import Request, Response
import json

def post_emojipass_handler(request: Request, csrf_token: str, emoji_pass: str, access_token: str):
    """POST handler for /emoji-pass endpoint."""

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
