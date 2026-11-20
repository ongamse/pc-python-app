# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through query_db's args parameter with ? placeholders; never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell-or-pickle -->
### sec-no-shell-or-pickle — No shell strings or pickle on request data

Run external programs with an argv list and shell=False, filtering output in Python. Use JSON, not pickle, for client-supplied serialized data.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-and-redirect-validation -->
### sec-path-and-redirect-validation — Validate file paths and redirect targets

Resolve user-supplied filenames and reject anything outside the per-user directory before file I/O. Route redirect targets through _safe_redirect_target in auth.py, which allows only same-origin relative paths.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secrets-and-headers -->
### sec-secrets-and-headers — Secrets from env, strict response headers

Load the Flask secret key from FLASK_SECRET_KEY and never commit it. Add trusted CORS origins via CORS_ALLOWED_ORIGINS instead of a wildcard, and keep script-src free of 'unsafe-inline' by serving JS from external files.
<!-- /harness-remediation -->
