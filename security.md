# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through query_db's args as ? placeholders with a tuple; never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-supplied file names

Sanitize filenames with werkzeug.utils.secure_filename and verify the resolved path's parent is the per-user data directory before writing; fail closed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Keep request data out of shell strings

Run commands with an argv list and shell=False, allowlist the user-supplied part with a fullmatch regex, and do any filtering in Python.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Never unpickle request data

Deserialize untrusted input as JSON with a size cap and structure check, and return 400 on malformed input.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load secrets from the environment

The Flask secret key comes from FLASK_SECRET_KEY, not source code; set it in deployments and rotate any key that was ever committed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Allowlist redirect targets

Route request-driven redirects through _safe_local_path in auth.py, which accepts only single-slash local paths and falls back to /.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-http-headers -->
### sec-http-headers — Strict CORS and CSP

Cross-origin access is an ALLOWED_ORIGINS exact-match allowlist (default same-origin, no wildcard) with Vary: Origin, and the CSP has no unsafe-inline, so put JavaScript in external static files.
<!-- /harness-remediation -->
