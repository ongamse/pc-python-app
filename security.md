# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass values to query_db() as a '?' placeholder plus an args tuple (as login_and_redirect does); never format request data into the SQL string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Never unpickle request data

Request payloads are decoded with base64 and json.loads, with a 400 on malformed input. Do not use pickle on anything a client can send.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-containment -->
### sec-path-containment — Contain user-derived file paths

Resolve any filename taken from a request and reject it unless it sits directly inside the per-user data directory (Path.resolve plus relative_to).
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — No shell for request data

Run subprocesses with a fixed argv list and shell=False, and filter their output in Python instead of building shell pipelines from request values.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Redirect only to same-site paths

Build redirects from request data through _safe_redirect_target in flask_webgoat/auth.py, which accepts only single-slash paths and falls back to '/'.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secrets-env -->
### sec-secrets-env — Load secrets from the environment

The Flask secret key comes from FLASK_SECRET_KEY, with an ephemeral random fallback. Never commit session keys, and set the variable in deployments so all workers share it.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-http-headers -->
### sec-http-headers — Keep CORS and CSP strict

Access-Control-Allow-Origin is set only for exact matches in CORS_ALLOWED_ORIGINS (empty by default), and script-src stays 'self'. Do not add a wildcard origin or 'unsafe-inline'; serve scripts as static files or use a nonce.
<!-- /harness-remediation -->
