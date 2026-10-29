import json
import base64
import re
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
    try:
        path.relative_to(base_dir)
    except ValueError:
        return jsonify({"error": "invalid filename"})
    if path.parent != base_dir:
        return jsonify({"error": "invalid filename"})
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if name is None or not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", name):
        return jsonify({"error": "invalid name parameter"})
    # No shell: run ps with a fixed argv and filter/extract in Python.
    res = subprocess.run(
        ["ps", "aux"],
        shell=False,
        capture_output=True,
        check=False,
    )
    if res.stdout is None:
        return jsonify({"error": "no stdout returned"})
    out = res.stdout.decode("utf-8")
    names = []
    for line in out.split("\n"):
        if name in line:
            fields = line.split()
            names.append(fields[10] if len(fields) > 10 else "")
    names.append("")
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    pickled = request.form.get('pickled')
    if pickled is None:
        return jsonify({"error": "pickled parameter is required"})
    try:
        data = base64.urlsafe_b64decode(pickled)
        # JSON is a data-only format; it cannot instantiate arbitrary objects.
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, TypeError):
        return jsonify({"error": "invalid data"})
    return jsonify({"success": True, "description": str(deserialized)})
