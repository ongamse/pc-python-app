import json
import base64
from pathlib import Path
import subprocess

from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename

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

    safe_name = secure_filename(filename_param)
    if not safe_name:
        return jsonify({"error": "invalid filename parameter"})
    filename = safe_name + ".txt"
    base_dir = user_dir_path.resolve()
    path = (base_dir / filename).resolve()
    if path.parent != base_dir:
        return jsonify({"error": "invalid filename parameter"})
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name parameter is required"})
    # No shell: fixed argv for ps; user input is only used as an in-process
    # fixed-string filter and never reaches a command line.
    res = subprocess.run(
        ["ps", "aux"],
        shell=False,
        capture_output=True,
    )
    if res.stdout is None:
        return jsonify({"error": "no stdout returned"})
    out = res.stdout.decode("utf-8")
    names = []
    for line in out.split("\n"):
        if name in line:
            fields = line.split()
            # equivalent of awk '{print $11}'
            names.append(fields[10] if len(fields) > 10 else "")
    names.append("")
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    # The payload is a urlsafe-base64 encoded JSON document (a safe data-only
    # format); arbitrary object deserialization is never performed.
    encoded = request.form.get("pickled")
    if not encoded:
        return jsonify({"error": "pickled parameter is required"})
    try:
        data = base64.urlsafe_b64decode(encoded)
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return jsonify({"error": "invalid payload: expected base64 encoded JSON"})
    if not _is_plain_json_value(deserialized):
        return jsonify({"error": "invalid payload structure"})
    return jsonify({"success": True, "description": str(deserialized)})


def _is_plain_json_value(value, depth=0):
    """Validate that a decoded value only contains plain JSON types."""
    if depth > 20:
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
