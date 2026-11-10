from urllib.parse import urlparse

from flask import Blueprint, request, jsonify, session, redirect
from . import query_db

bp = Blueprint("auth", __name__)


def _safe_redirect_target(url, default="/"):
    """Return url only if it is a same-site relative path, else default."""
    if not isinstance(url, str) or not url.startswith("/"):
        return default
    # Reject scheme-relative (//host), backslash tricks (/\host) and control chars.
    if url.startswith("//") or "\\" in url or any(ord(c) < 32 or ord(c) == 127 for c in url):
        return default
    parts = urlparse(url)
    if parts.scheme or parts.netloc:
        return default
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
