# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values to query_db as bound args with ? placeholders (login and create_user now do); never build SQL with % formatting.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-file-path -->
### sec-file-path — Confine user-named file writes

Sanitize user filenames with werkzeug.utils.secure_filename and verify the resolved path stays inside the user's data directory, failing closed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Keep request data out of shells

Run subprocess with an argv list and shell=False, and filter output in Python instead of piping user input through grep or awk.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Do not unpickle request data

Use JSON (validated, base64-wrapped if needed) as the wire format for client-supplied objects; never call pickle.loads on request input.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load secrets from the environment

The Flask secret key comes from FLASK_SECRET_KEY, with a per-process random fallback. Set it in deployment and never commit a key.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-redirect-allowlist -->
### sec-redirect-allowlist — Allowlist redirect targets

Route redirect targets through _safe_redirect_target in auth.py, which accepts only same-origin relative paths and falls back to /.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-http-headers -->
### sec-http-headers — Keep CORS and CSP strict

CORS origins come from the CORS_ALLOWED_ORIGINS allowlist (no wildcard) and the CSP uses script-src 'self'. Put scripts in external files instead of re-adding unsafe-inline.
<!-- /harness-remediation -->
