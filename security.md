# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through query_db's args tuple with ? placeholders; never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell-or-pickle -->
### sec-no-shell-or-pickle — No shell strings or pickle on request data

Run subprocesses with an argv list and shell=False and filter output in Python. Parse request payloads with JSON, never pickle.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-and-redirect-validation -->
### sec-path-and-redirect-validation — Validate paths and redirect targets

Resolve user-supplied filenames and require them to sit inside the intended base directory. Redirect only to same-site relative paths checked by _is_safe_redirect_target.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-config-secrets-and-headers -->
### sec-config-secrets-and-headers — Secrets from env, strict CORS and CSP

Load the Flask secret key from FLASK_SECRET_KEY and add trusted CORS origins through CORS_ALLOWED_ORIGINS, never a wildcard. Keep the CSP free of 'unsafe-inline' and put scripts in external files.
<!-- /harness-remediation -->
