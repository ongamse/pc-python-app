# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Callers of query_db must pass values through its args tuple with ? placeholders; never format request values into SQL strings.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell-or-unpickle -->
### sec-no-shell-or-unpickle — No shell strings or unsafe deserialization

Run subprocesses with argv lists and shell=False after allowlist validation, and parse request data with json, never pickle.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-derived file paths

Resolve user-derived paths and reject them unless they stay inside the intended per-user directory.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Redirect only to same-site paths

Route any redirect target taken from request data through auth._safe_redirect_target, which only allows relative same-site paths.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-from-env -->
### sec-secret-from-env — Load secrets from the environment

app.secret_key comes from FLASK_SECRET_KEY, never from source. Rotate any key that was previously committed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-csp -->
### sec-cors-csp — Keep CORS and CSP strict

Add cross-origin consumers through CORS_ALLOWED_ORIGINS instead of a wildcard, and keep script-src 'self'; use static files or nonces rather than 'unsafe-inline'.
<!-- /harness-remediation -->
