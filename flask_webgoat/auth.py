from urllib.parse import urlparse

from flask import Blueprint, request, jsonify, session, redirect
from . import query_db

bp = Blueprint("auth", __name__)


def _is_safe_redirect_path(url):
    """Allow only same-site absolute paths (e.g. "/home"); reject schemes,
    hosts, protocol-relative "//host" and backslash/control-char tricks."""
    if not url or not url.startswith("/") or url.startswith("//"):
        return False
    if "\\" in url or any(ord(c) < 0x20 or ord(c) == 0x7F for c in url):
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

    query = "SELECT id, username, access_level FROM user WHERE username = ? AND password = ?"
    result = query_db(query, (username, password), True)
    if result is None:
        if not _is_safe_redirect_path(url):
            return jsonify({"error": "url must be a relative path on this site"}), 400
        return redirect(url)
    session["user_info"] = (result[0], result[1], result[2])
    return jsonify({"success": True})
