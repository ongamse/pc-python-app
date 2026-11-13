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
    user_dir = "data/" + str(user_id)
    user_dir_path = Path(user_dir)
    if not user_dir_path.exists():
        user_dir_path.mkdir()

    filename = filename_param + ".txt"
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
    if name is None:
        return jsonify({"error": "name parameter is required"})
    # Fixed argv, no shell: request data is never interpreted by a shell.
    # Filtering (grep) and column extraction (awk '{print $11}') are done
    # in Python instead of in a shell pipeline.
    res = subprocess.run(
        ["ps", "aux"],
        shell=False,
        capture_output=True,
        check=False,
    )
    if res.stdout is None:
        return jsonify({"error": "no stdout returned"})
    out = res.stdout.decode("utf-8")
    matches = []
    for line in out.splitlines():
        if name not in line:
            continue
        fields = line.split()
        matches.append(fields[10] if len(fields) > 10 else "")
    names = "".join(match + "\n" for match in matches).split("\n")
    return jsonify({"success": True, "names": names})


@bp.route("/deserialized_descr", methods=["POST"])
def deserialized_descr():
    # The payload is a urlsafe-base64 encoded JSON document. JSON can only
    # yield plain data types, so decoding cannot execute attacker code.
    payload = request.form.get("pickled")
    if payload is None:
        return jsonify({"error": "pickled parameter is required"})
    try:
        data = base64.urlsafe_b64decode(payload)
        deserialized = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return jsonify({"error": "pickled parameter must be base64-encoded JSON"})
    return jsonify({"success": True, "description": str(deserialized)})
