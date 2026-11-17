# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values to query_db as a params tuple with ? placeholders; never format them into the SQL string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-contain -->
### sec-path-contain — Contain user-supplied file paths

Resolve any path built from request data and check it stays inside the intended per-user directory before opening it.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — No shell for process commands

Run subprocesses with a fixed argv and shell=False, and do filtering of the output in Python rather than interpolating request data into a shell string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Never unpickle request data

Use JSON for data interchange with clients; pickle.loads on request input allows arbitrary code execution.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load secrets from the environment

The Flask secret key comes from FLASK_SECRET_KEY or SECRET_KEY. Never commit a key; rotate any key that was ever committed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Allow only local redirect targets

Send user-supplied redirect targets through _safe_local_redirect_target in auth.py, which accepts same-origin relative paths only.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-allowlist -->
### sec-cors-allowlist — Use a CORS origin allowlist

Extend CORS_ALLOWED_ORIGINS with exact trusted origins instead of using a wildcard Access-Control-Allow-Origin.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-csp-no-inline -->
### sec-csp-no-inline — Keep CSP script-src free of unsafe-inline

Put JavaScript in external static files served from 'self' so script-src does not need 'unsafe-inline'.
<!-- /harness-remediation -->
