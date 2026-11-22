# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through query_db's args tuple with ? placeholders. Never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Never unpickle request data

Untrusted payloads are parsed with a data-only format (base64-encoded JSON), never pickle.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — No shell for user input

Run subprocesses with an argv list and shell=False, and filter output in Python so request values never reach a shell.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-controlled paths

Resolve the target with Path.resolve() and require relative_to() the per-user directory, which rejects .., absolute paths and symlink escapes.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Allowlist redirect targets

Validate redirect URLs with _is_safe_redirect_path in flask_webgoat/auth.py, which accepts only same-site paths and returns 400 otherwise.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Secrets come from the environment

The Flask secret key is read from FLASK_SECRET_KEY, with no committed literal. Set it in every deployment and rotate the old key, which remains in git history.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-http-headers -->
### sec-http-headers — Strict CORS and CSP

CORS origins come from the CORS_ALLOWED_ORIGINS allowlist (never '*'), and the CSP uses script-src 'self' without unsafe-inline. Keep JavaScript in external static files.
<!-- /harness-remediation -->
