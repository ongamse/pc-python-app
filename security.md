# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

query_db(query, args) in flask_webgoat/__init__.py binds parameters via cursor.execute. Callers must use ? placeholders and pass request values through args, never % formatting or concatenation.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Never deserialize request data with pickle

Request payloads are decoded with json.loads, not pickle.loads. Use a data-only format for anything client-supplied.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-influenced file paths

Resolve the path with Path.resolve() and require it to be a direct child of the intended data directory before reading or writing; reject anything else.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Keep shell out of command execution

Run subprocesses with a fixed argv and shell=False, and filter output in Python. Request data must never be concatenated into a command string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load secrets from the environment

The Flask secret key is read from FLASK_SECRET_KEY and never committed as a literal. Supply it through env or a secrets manager.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Allowlist redirect targets

Redirects to user-supplied URLs go through _safe_redirect_target in auth.py, which allows only same-site relative paths and falls back to /.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-strict-headers -->
### sec-strict-headers — Keep CORS and CSP strict

CORS origins come from the CORS_ALLOWED_ORIGINS allowlist (no wildcard) and script-src stays 'self' without 'unsafe-inline'. Put scripts in external static files, not inline blocks or handlers.
<!-- /harness-remediation -->
