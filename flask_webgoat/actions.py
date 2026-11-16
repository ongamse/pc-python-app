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
    base_path = user_dir_path.resolve()
    path = (base_path / filename).resolve()
    if path.parent != base_path:
        return jsonify({"error": "invalid filename"}), 400
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if name is None:
        return jsonify({"error": "name parameter is required"}), 400
    # No shell: run ps with a fixed argv and filter/extract the command
    # column in Python so user input never reaches a command interpreter.
    res = subprocess.run(
        ["ps", "aux"],
        shell=False,
        capture_output=True,
    )
    if res.stdout is None:
        return jsonify({"error": "no stdout returned"})
    lines = res.stdout.decode("utf-8", errors="replace").split("\n")
    names = []
    for line in lines:
        if name not in line:
            continue
        fields = line.split()
        names.append(fields[10] if len(fields) > 10 else "")
    names.append("")
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    encoded = request.form.get("pickled")
    if encoded is None:
        return jsonify({"error": "pickled parameter is required"}), 400
    # Safe data format: base64-encoded JSON (pure data, no code execution).
    try:
        data = base64.urlsafe_b64decode(encoded)
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return jsonify({"error": "invalid payload, expected base64-encoded JSON"}), 400
    return jsonify({"success": True, "description": str(deserialized)})
