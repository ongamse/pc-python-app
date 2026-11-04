# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through query_db's args tuple using ? placeholders, never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — No pickle on request data

Do not unpickle client-supplied data; use a data-only format such as JSON and return an error on malformed input.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — No shell for request data

Run subprocesses with an argv list and shell=False, and filter output in Python instead of building shell pipelines from request arguments.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-supplied file names

Resolve the target path and require it to be a direct child of the intended directory before writing, rejecting anything else.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-redirect-allowlist -->
### sec-redirect-allowlist — Allowlist redirect targets

Route redirects built from user input through _safe_redirect_target, which allows only same-site relative paths and falls back to /.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load secrets from the environment

Read the Flask secret key from FLASK_SECRET_KEY and fail closed when it is unset; never commit a fallback value, and rotate any key that was committed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-allowlist -->
### sec-cors-allowlist — No wildcard CORS

Echo the request Origin only on an exact match against CORS_ALLOWED_ORIGINS and send no CORS header by default.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-csp-strict -->
### sec-csp-strict — Keep CSP strict

Keep script-src at 'self' with object-src 'none' and base-uri 'self'; put any new JavaScript in external static files rather than re-adding 'unsafe-inline'.
<!-- /harness-remediation -->
