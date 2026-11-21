# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through query_db's args parameter with ? placeholders; never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-unsafe-deserialize -->
### sec-no-unsafe-deserialize — No pickle on request data

Parse request payloads with json.loads (or safe loaders) and handle malformed input; never use pickle or unsafe yaml on user data.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell-with-input -->
### sec-no-shell-with-input — No shell with request data

Run subprocesses with a fixed argv and shell=False, and do filtering in Python so request values never reach a shell.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-confine-user-paths -->
### sec-confine-user-paths — Confine user-supplied paths

Sanitize filenames with secure_filename and verify the resolved path stays inside the intended directory before opening it.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Redirect only to same-site paths

Route redirects built from request input through _safe_redirect_target in flask_webgoat/auth.py, which falls back to / for external or malformed targets.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secrets-from-env -->
### sec-secrets-from-env — Keep secrets out of source

Read the Flask secret key from FLASK_SECRET_KEY and rotate the previously committed value, since it remains in git history.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-headers-restrictive -->
### sec-headers-restrictive — Keep CORS and CSP restrictive

Add cross-origin consumers through the CORS_ALLOWED_ORIGINS allowlist, never a wildcard, and serve scripts from static files rather than re-adding unsafe-inline to script-src.
<!-- /harness-remediation -->
