from urllib.parse import urlparse

from flask import Blueprint, request, jsonify, session, redirect
from . import query_db

bp = Blueprint("auth", __name__)


def _safe_local_path(target, default="/"):
    """Return target only if it is a same-site relative path, else default."""
    if not isinstance(target, str) or not target.startswith("/"):
        return default
    # Reject protocol-relative URLs, backslash tricks and control characters.
    if target.startswith("//") or "\\" in target:
        return default
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in target):
        return default
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc:
        return default
    return target


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
        return redirect(_safe_local_path(url))
    session["user_info"] = (result[0], result[1], result[2])
    return jsonify({"success": True})
