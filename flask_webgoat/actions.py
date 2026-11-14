import base64
import json
from pathlib import Path
import re
import subprocess

from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename

bp = Blueprint("actions", __name__)

PROCESS_NAME_RE = re.compile(r"[A-Za-z0-9_.\-]{1,64}")


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
        return jsonify({"error": "invalid filename"})
    filename = safe_name + ".txt"
    base_dir = user_dir_path.resolve()
    path = (base_dir / filename).resolve()
    if path.parent != base_dir:
        return jsonify({"error": "invalid filename"})
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if name is None:
        return jsonify({"error": "name parameter is required"})
    if not PROCESS_NAME_RE.fullmatch(name):
        return jsonify({"error": "invalid name"})
    # Fixed argv, no shell; filtering and column extraction happen in Python
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
            fields = line.split()
            out += (fields[10] if len(fields) > 10 else "") + "\n"
    names = out.split("\n")
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    # The payload is urlsafe-base64 encoded JSON; JSON cannot instantiate
    # arbitrary objects, unlike pickle.
    encoded = request.form.get("pickled")
    if encoded is None:
        return jsonify({"error": "pickled parameter is required"})
    try:
        data = base64.urlsafe_b64decode(encoded)
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, TypeError):
        return jsonify({"error": "invalid payload"})
    if not isinstance(deserialized, dict):
        return jsonify({"error": "payload must be a JSON object"})
    return jsonify({"success": True, "description": str(deserialized)})
