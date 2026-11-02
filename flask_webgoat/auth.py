from urllib.parse import urlsplit

from flask import Blueprint, request, jsonify, session, redirect
from . import query_db

bp = Blueprint("auth", __name__)

_DEFAULT_REDIRECT = "/"


def _safe_redirect_target(url):
    """Allow only same-site relative paths; otherwise fall back to the default."""
    if not isinstance(url, str) or not url.startswith("/"):
        return _DEFAULT_REDIRECT
    # Reject scheme-relative ("//host"), backslash tricks ("/\host") and
    # control characters/whitespace that browsers may normalize away.
    if url.startswith("//") or "\\" in url:
        return _DEFAULT_REDIRECT
    if any(ch.isspace() or ord(ch) < 0x20 or ord(ch) == 0x7F for ch in url):
        return _DEFAULT_REDIRECT
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        return _DEFAULT_REDIRECT
    return url


@bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None or password is None:
        return (
            jsonify({"error": "username and password parameter have to be provided"}),
            400,
        )

    query = "SELECT id, username, access_level FROM user WHERE username = ? AND password = ?"
    result = query_db(query, (username, password), True)
    if result is None:
        return jsonify({"bad_login": True}), 400
    session["user_info"] = (result[0], result[1], result[2])
    return jsonify({"success": True})


@bp.route("/login_and_redirect")
def login_and_redirect():
    username = request.args.get("username")
    password = request.args.get("password")
    url = request.args.get("url")
    if username is None or password is None or url is None:
        return (
            jsonify(
                {"error": "username, password, and url parameters have to be provided"}
            ),
            400,
        )

    query = "SELECT id, username, access_level FROM user WHERE username = ? AND password = ?"
    result = query_db(query, (username, password), True)
    if result is None:
        return redirect(_safe_redirect_target(url))
    session["user_info"] = (result[0], result[1], result[2])
    return jsonify({"success": True})
