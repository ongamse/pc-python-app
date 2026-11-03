# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Request values in this repo reach SQL through ? placeholders and an args tuple passed to query_db, never through % string formatting.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Never unpickle request data

Untrusted request fields are parsed as JSON (data-only), not with pickle.loads.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-key-env -->
### sec-secret-key-env — Load the Flask secret key from the environment

app.secret_key comes from FLASK_SECRET_KEY with a random per-process fallback; never commit a session key, and rotate any key that was in git history.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-named files to their directory

Resolve user-supplied filenames with pathlib and reject any path that does not stay directly inside the intended directory.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Redirect only to same-site paths

Redirect targets from request input go through _safe_local_path in flask_webgoat/auth.py, which allows only single-slash local paths and falls back to /.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-allowlist -->
### sec-cors-allowlist — Use an origin allowlist for CORS

Access-Control-Allow-Origin is set only for origins listed in CORS_ALLOWED_ORIGINS (default none); extend that variable instead of reintroducing a wildcard.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Do not build shell commands from request data

Run subprocesses with a fixed argv and shell=False, and do filtering in Python so request values never reach a shell.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-strict-csp -->
### sec-strict-csp — Keep the CSP free of unsafe-inline

The policy is default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'. Put new JavaScript in static files, not inline.
<!-- /harness-remediation -->
