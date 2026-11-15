# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Request values reach SQL only through query_db's args parameter with ? placeholders, as login(), create_user() and login_and_redirect() now do. Never format user input into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-containment -->
### sec-path-containment — Contain user-supplied file paths

Resolve the per-user directory and the final path, and reject anything that is not inside the base directory before opening a file. Never concatenate request values into a path.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell-or-pickle -->
### sec-no-shell-or-pickle — No shell strings or pickle on request data

Run external programs with a fixed argv and shell=False, and filter output in Python. Parse request payloads with data-only formats such as JSON, never pickle.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secrets-from-env -->
### sec-secrets-from-env — Load secrets from the environment

The Flask session key comes from FLASK_SECRET_KEY, with a per-process random fallback. Never commit session keys, and rotate any value that was committed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-redirect-allowlist -->
### sec-redirect-allowlist — Validate redirect targets

Pass user-supplied redirect targets through _safe_redirect_target() in auth.py, which accepts same-site paths only and falls back to /status.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-strict-headers -->
### sec-strict-headers — Keep CORS and CSP strict

Allow cross-origin requests only for origins listed in CORS_ALLOWED_ORIGINS, never '*'. Keep the CSP free of 'unsafe-inline'; serve any needed inline JS from a static file or use nonces.
<!-- /harness-remediation -->
