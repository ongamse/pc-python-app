import base64
import json
import re
from pathlib import Path
import subprocess

from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename

bp = Blueprint("actions", __name__)

PROCESS_NAME_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")
MAX_SERIALIZED_LEN = 8192


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
    base_dir = user_dir_path.resolve()
    path = (base_dir / (safe_name + ".txt")).resolve()
    if path.parent != base_dir:
        return jsonify({"error": "invalid filename"})
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if name is None or not PROCESS_NAME_RE.fullmatch(name):
        return jsonify({"error": "invalid name parameter"})
    # No shell: fixed argv, filtering done in Python on the validated name.
    res = subprocess.run(
        ["ps", "aux"],
        shell=False,
        capture_output=True,
        check=False,
    )
    if res.stdout is None:
        return jsonify({"error": "no stdout returned"})
    out = res.stdout.decode("utf-8", errors="replace")
    names = []
    for line in out.split("\n"):
        if name in line:
            fields = line.split()
            names.append(fields[10] if len(fields) > 10 else "")
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    encoded = request.form.get("serialized")
    if encoded is None:
        encoded = request.form.get("pickled")
    if not encoded:
        return jsonify({"error": "serialized parameter is required"}), 400
    if len(encoded) > MAX_SERIALIZED_LEN:
        return jsonify({"error": "serialized parameter too large"}), 400
    try:
        padded = encoded + "=" * (-len(encoded) % 4)
        data = base64.urlsafe_b64decode(padded.encode("ascii"))
        # JSON only: parsing cannot instantiate arbitrary objects.
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeError):
        return jsonify({"error": "invalid serialized data"}), 400
    if not isinstance(deserialized, (dict, list, str, int, float, bool)):
        return jsonify({"error": "invalid serialized data"}), 400
    return jsonify({"success": True, "description": str(deserialized)})
