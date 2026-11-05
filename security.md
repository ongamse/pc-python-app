# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Queries in auth.py and users.py were built with string formatting and passed no arguments to query_db. Use ? placeholders and pass a parameter tuple, as login_and_redirect and ui.py already do.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-named file paths

Resolve any file path built from request input and require it to stay inside the user's own directory (as log_entry now does). Reject names that escape it.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Never pass request data to a shell

Run subprocesses with an argv list and shell=False, and filter output in Python. grep_processes no longer builds a shell pipeline from the request.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Do not unpickle request data

Use JSON or another data-only format for anything that arrives in a request. deserialized_descr now parses with json.loads instead of pickle.loads.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secrets-env -->
### sec-secrets-env — Load secrets from the environment

The Flask secret key is read from FLASK_SECRET_KEY, with a per-process random fallback. Never commit a live key, and rotate any key that was ever committed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Validate redirect targets

Route user-controlled redirects through _safe_redirect_target in auth.py, which allows only same-site relative paths and falls back to /.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-csp -->
### sec-cors-csp — Keep CORS and CSP strict

Allow cross-origin access only for origins listed in CORS_ALLOWED_ORIGINS, never with a wildcard. Keep script-src 'self' and move any script into external static files instead of re-adding unsafe-inline.
<!-- /harness-remediation -->
