# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through query_db's args tuple with ? placeholders; never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-containment -->
### sec-path-containment — Contain user-supplied file paths

Resolve the target path and require it to sit directly inside the per-user data directory before opening it; this rejects .., absolute paths and separators.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Keep request data out of shells

Run subprocesses with a fixed argv and shell=False, and filter output in Python instead of interpolating request arguments into a shell pipeline.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Do not unpickle request data

Parse client-supplied serialized objects as JSON, which yields plain data only; pickle.loads on request input allows code execution.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load the Flask secret key from the environment

app.secret_key comes from FLASK_WEBGOAT_SECRET_KEY, with a random per-process fallback. Never commit a key, and rotate any key that was previously committed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-redirect-relative -->
### sec-redirect-relative — Redirect only to same-site paths

Route user-supplied redirect targets through _is_safe_redirect_target in flask_webgoat/auth.py, which allows only single-slash relative paths and returns 400 otherwise.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-allowlist -->
### sec-cors-allowlist — Use an origin allowlist for CORS

Echo the request Origin only when it exactly matches CORS_ALLOWED_ORIGINS (empty by default) and send Vary: Origin; never use a wildcard origin.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-csp-no-inline -->
### sec-csp-no-inline — Keep the CSP free of unsafe-inline

script-src stays 'self' with no inline allowance; put any new JavaScript in external files under static rather than inline script or event handlers.
<!-- /harness-remediation -->
