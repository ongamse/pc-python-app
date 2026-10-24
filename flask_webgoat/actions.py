import os
import json
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

    safe_name = os.path.basename(filename_param)
    if not safe_name:
        return jsonify({"error": "invalid filename"})
    filename = safe_name + ".txt"
    path = (user_dir_path / filename).resolve()
    if not path.is_relative_to(user_dir_path.resolve()):
        return jsonify({"error": "invalid filename"})
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name parameter is required"})
    res = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
    )
    if res.stdout is None:
        return jsonify({"error": "no stdout returned"})
    out = res.stdout.decode("utf-8")
    names = []
    for line in out.split("\n"):
        if name in line:
            parts = line.split()
            if len(parts) >= 11:
                names.append(parts[10])
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    data = request.form.get('data')
    if data is None:
        return jsonify({"error": "data parameter is required"})
    deserialized = json.loads(data)
    return jsonify({"success": True, "description": str(deserialized)})
