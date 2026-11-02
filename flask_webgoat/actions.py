import base64
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
    user_dir_path = Path("data") / str(user_id)
    if not user_dir_path.exists():
        user_dir_path.mkdir()

    # Only a plain file name is allowed: no path separators, no traversal,
    # no absolute paths, no NUL bytes.
    if (
        not filename_param
        or "/" in filename_param
        or "\\" in filename_param
        or "\x00" in filename_param
        or filename_param in (".", "..")
        or Path(filename_param).is_absolute()
    ):
        return jsonify({"error": "invalid filename"}), 400

    base_dir = user_dir_path.resolve()
    path = (base_dir / (filename_param + ".txt")).resolve()
    # Confine the resolved path to the user's directory (also defeats symlinks).
    if path.parent != base_dir:
        return jsonify({"error": "invalid filename"}), 400
    with path.open("w", encoding="utf-8") as open_file:
        open_file.write(text_param)
    return jsonify({"success": True})


@bp.route("/grep_processes")
def grep_processes():
    name = request.args.get("name")
    if not name or "\x00" in name:
        return jsonify({"error": "name parameter is required"}), 400
    # No shell: run a fixed argv and do the grep/awk filtering in Python so
    # user input is never interpreted as a command.
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
    for line in out.splitlines():
        if name in line:
            fields = line.split()
            # equivalent of awk '{print $11}'
            names.append(fields[10] if len(fields) >= 11 else "")
    names.append("")
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    # The payload is a urlsafe-base64 encoded JSON document. JSON is a
    # data-only format, so decoding it cannot execute code.
    encoded = request.form.get("pickled")
    if not encoded:
        return jsonify({"error": "pickled parameter is required"}), 400
    try:
        data = base64.urlsafe_b64decode(encoded)
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return jsonify({"error": "invalid payload"}), 400
    return jsonify({"success": True, "description": str(deserialized)})
