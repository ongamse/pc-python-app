# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-pickle-json -->
### sec-pickle-json — Never unpickle request data

/deserialized_descr passed request data to pickle.loads, which allows remote code execution. Parse request data with a data-only format such as JSON and validate the resulting type.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-key-env -->
### sec-secret-key-env — Load the Flask secret key from the environment

create_app() no longer hardcodes app.secret_key; it reads FLASK_SECRET_KEY and falls back to a random per-process key. Set FLASK_SECRET_KEY in deployments and rotate the old key, since it remains in git history.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Resolve and confine user-influenced file paths

Filenames from requests are resolved and rejected unless their parent is the user's own data directory, which blocks ../ and absolute-path escapes. Apply the same check to any new file access driven by user input.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Route redirects through _safe_redirect_target

Redirect targets from request parameters must go through _safe_redirect_target in flask_webgoat/auth.py, which only allows same-site relative paths and otherwise falls back to /status.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-allowlist -->
### sec-cors-allowlist — Use an origin allowlist for CORS

run.py echoes the request Origin only when it exactly matches an entry in the CORS_ALLOWED_ORIGINS env var, never uses a wildcard, and never sets Allow-Credentials. Configure trusted origins through the environment.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Do not build shell strings from request args

grep_processes runs ps with a fixed argv and shell=False and filters the output in Python. Never concatenate request values into a shell command; filter in-process instead.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-strict-csp -->
### sec-strict-csp — Keep the CSP strict

The Content-Security-Policy is default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'. Keep JavaScript in static files and do not re-add unsafe-inline or unsafe-eval.
<!-- /harness-remediation -->
