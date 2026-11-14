# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

query_db already binds args through sqlite3 execute(query, args). Callers must pass ? placeholders plus a params tuple, never format request data into the SQL string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-shell-argv -->
### sec-shell-argv — No shell strings with request data

Run external programs with subprocess argv lists and shell=False, and allowlist request-supplied values. Do filtering in Python rather than piping through grep or awk.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-contain -->
### sec-path-contain — Contain request-derived file paths

Pass request-supplied filenames through werkzeug secure_filename and check that the resolved path stays directly inside the user's data directory before opening it.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Never unpickle request data

Parse request payloads as JSON and validate the parsed structure. pickle.loads on attacker-controlled data is remote code execution.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load secrets from the environment

The Flask secret key comes from FLASK_SECRET_KEY, with a random per-process fallback. Never commit a literal key, and rotate any key that was already in git history.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Route redirects through the local-path check

Redirect targets from request data go through _safe_redirect_target in flask_webgoat/auth.py, which allows only same-site relative paths and falls back to /status.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-csp -->
### sec-cors-csp — Keep CORS allowlisted and CSP strict

Cross-origin access is granted only to origins in ALLOWED_ORIGINS, never a wildcard. script-src stays 'self'; if inline scripts are added, move them to static files or use a per-request nonce.
<!-- /harness-remediation -->
