# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass request values through query_db's args tuple with ? placeholders; never format them into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-file-path-confine -->
### sec-file-path-confine — Confine user-supplied file paths

Sanitize filenames with secure_filename and verify the resolved path stays inside the per-user data directory, failing closed otherwise.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Keep user input out of shells

Run subprocesses with argv lists and shell=False, and do any filtering in Python rather than through a shell pipeline.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-deserialize -->
### sec-safe-deserialize — Never unpickle request data

Use JSON for client-supplied serialized objects; pickle.loads on request data allows remote code execution.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load secrets from the environment

The Flask secret key comes from FLASK_SECRET_KEY, never from source. Keys that were committed remain in git history and must be rotated.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Validate redirect targets

Redirect only to same-site single-slash paths via _safe_local_path in flask_webgoat/auth.py; reject schemes, //host, backslashes and control characters.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-allowlist -->
### sec-cors-allowlist — No wildcard CORS

Responses are same-origin by default; add allowed origins through the CORS_ALLOWED_ORIGINS environment variable, never '*'.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-csp-no-inline -->
### sec-csp-no-inline — Strict Content-Security-Policy

Keep script-src 'self' without unsafe-inline and put any new JavaScript in external same-origin files.
<!-- /harness-remediation -->
