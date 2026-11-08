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
    path = (base_dir / filename).resolve()
    # Confine writes to the user's own directory (reject "..", separators, absolute paths).
    if path.parent != base_dir:
        return jsonify({"error": "invalid filename"})
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name parameter is required"})
    # Fixed argv, no shell: user input is never passed to a command interpreter.
    # The grep/awk filtering is done in Python instead of a shell pipeline.
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
            if len(fields) >= 11:
                names.append(fields[10])
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    encoded = request.form.get('pickled')
    if not encoded:
        return jsonify({"error": "pickled parameter is required"}), 400
    # Data-only format (base64url-encoded JSON); never executes code on load.
    try:
        data = base64.urlsafe_b64decode(encoded)
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return jsonify({"error": "invalid payload"}), 400
    if not isinstance(deserialized, (dict, list, str, int, float, bool)):
        return jsonify({"error": "invalid payload"}), 400
    return jsonify({"success": True, "description": str(deserialized)})
