# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through the args tuple of query_db(query, args) with ? placeholders. Never format user input into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-supplied file names

Resolve the target path and require it to be a direct child of the resolved per-user directory. Reject '..', separators and absolute paths.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — No shell for request-driven commands

Run commands with an argv list and shell=False, and filter output in Python. Never concatenate request data into a shell command string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — No pickle for client data

Use JSON for serialized objects that clients send. Never call pickle.loads on request data.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load signing keys from the environment

Read the Flask secret key from FLASK_SECRET_KEY and never commit it. A key that was committed must be rotated, since it remains in git history.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Redirect only to local paths

Route redirect targets through _safe_redirect_target in flask_webgoat/auth.py. It allows only same-site relative paths and defaults to '/'.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-allowlist -->
### sec-cors-allowlist — Allowlist CORS origins

Reflect the request Origin only when it is listed in CORS_ALLOWED_ORIGINS, and never use a wildcard. The default is same-origin only.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-csp-no-inline -->
### sec-csp-no-inline — Keep script-src free of unsafe-inline

Put new JavaScript in external static files or use nonces. Do not re-add 'unsafe-inline' to the CSP script-src.
<!-- /harness-remediation -->
