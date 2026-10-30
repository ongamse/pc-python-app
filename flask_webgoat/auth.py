from urllib.parse import urlparse

from flask import Blueprint, request, jsonify, session, redirect
from . import query_db

bp = Blueprint("auth", __name__)


def _is_safe_redirect_target(url):
    """Allow only same-site relative paths (e.g. "/home?x=1")."""
    if not isinstance(url, str) or not url.startswith("/"):
        return False
    # Protocol-relative URLs and backslash tricks ("//host", "/\host")
    if url.startswith("//") or "\\" in url:
        return False
    # Control characters (browsers strip tabs/newlines inside URLs)
    if any(ord(c) < 0x20 or ord(c) == 0x7F for c in url):
        return False
    parsed = urlparse(url)
    return not parsed.scheme and not parsed.netloc


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

    if not _is_safe_redirect_target(url):
        return jsonify({"error": "url must be a same-site relative path"}), 400

    query = "SELECT id, username, access_level FROM user WHERE username = ? AND password = ?"
    result = query_db(query, (username, password), True)
    if result is None:
        return redirect(url)
    session["user_info"] = (result[0], result[1], result[2])
    return jsonify({"success": True})
