import json
import base64
from pathlib import Path
import subprocess

from flask import Blueprint, request, jsonify, session

bp = Blueprint("actions", __name__)


@bp.route("/message", methods=["POST"])
def log_entry():
    user_info = session.get("user_info", None)
    if user_info is None:
        return jsonify({"error": "no user_info found in session"})
    access_level = user_info[2]
    if access_level > 2:
        return jsonify({"error": "access level < 2 is required for this action"})
    filename_param = request.form.get("filename")
    if filename_param is None:
        return jsonify({"error": "filename parameter is required"})
    text_param = request.form.get("text")
    if text_param is None:
        return jsonify({"error": "text parameter is required"})

    user_id = user_info[0]
    user_dir = "data/" + str(user_id)
    user_dir_path = Path(user_dir)
    if not user_dir_path.exists():
        user_dir_path.mkdir()

    filename = filename_param + ".txt"
    base_dir = user_dir_path.resolve()
    try:
        path = (base_dir / filename).resolve()
        path.relative_to(base_dir)
    except ValueError:
        return jsonify({"error": "invalid filename"})
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if name is None:
        return jsonify({"error": "name parameter is required"})
    # No shell: run ps with a fixed argv and filter/extract in Python.
    res = subprocess.run(
        ["ps", "aux"],
        shell=False,
        capture_output=True,
    )
    if res.stdout is None:
        return jsonify({"error": "no stdout returned"})
    lines = res.stdout.decode("utf-8", errors="replace").split("\n")
    out = ""
    for line in lines:
        if name in line:
            # equivalent of awk '{print $11}'
            fields = line.split()
            out += (fields[10] if len(fields) > 10 else "") + "\n"
    names = out.split("\n")
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    # The payload is a urlsafe-base64 encoded JSON document (never pickle).
    payload = request.form.get('pickled')
    if payload is None:
        return jsonify({"error": "pickled parameter is required"}), 400
    try:
        data = base64.urlsafe_b64decode(payload)
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return jsonify({"error": "invalid payload: expected base64-encoded JSON"}), 400
    if not _is_plain_json_value(deserialized):
        return jsonify({"error": "invalid payload structure"}), 400
    return jsonify({"success": True, "description": str(deserialized)})


def _is_plain_json_value(value, depth=0):
    """Allow only JSON scalars, lists and string-keyed dicts of bounded depth."""
    if depth > 10:
        return False
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, list):
        return all(_is_plain_json_value(v, depth + 1) for v in value)
    if isinstance(value, dict):
        return all(
            isinstance(k, str) and _is_plain_json_value(v, depth + 1)
            for k, v in value.items()
        )
    return False
