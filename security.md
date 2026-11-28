# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values to query_db through its args tuple with ? placeholders; never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Never build shell commands from request input

Run external programs with an argv list and shell disabled, and do text filtering in Python so user input never reaches a shell.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Never unpickle request data

Parse untrusted payloads with a data-only format such as JSON and validate the structure before use.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-contain -->
### sec-path-contain — Contain user-influenced file paths

Resolve the target path and verify it stays inside the intended base directory before opening it.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-redirect-allowlist -->
### sec-redirect-allowlist — Allowlist redirect targets

Only redirect to same-site relative paths via _safe_redirect_target in auth.py; fall back to / for anything else.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secrets-env -->
### sec-secrets-env — Keep secrets out of source

Load the Flask secret key from FLASK_SECRET_KEY instead of committing it; the previously committed key is in git history and must be rotated.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-web-headers -->
### sec-web-headers — Keep CORS and CSP strict

Configure allowed CORS origins through CORS_ALLOWED_ORIGINS rather than a wildcard, and keep script-src limited to 'self' with scripts in external files.
<!-- /harness-remediation -->
