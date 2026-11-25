# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Request values reach SQL through `?` placeholders and an args tuple passed to `query_db`, never through `%` string formatting.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Keep request data out of shells

Run external programs with an argv list and `shell=False`, and filter output in Python instead of building a shell pipeline from request data.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-influenced file paths

Resolve the final path and require it to stay inside the intended directory with `Path.resolve()` and `relative_to()` before reading or writing.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Do not deserialize request data with pickle

Parse untrusted payloads as JSON and validate their shape; `pickle.loads` on request data is remote code execution.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Redirect only to local paths

Validate redirect targets with `_is_safe_local_path` in `flask_webgoat/auth.py` (single leading `/`, no scheme, host, `//` or backslash) and reuse it for any new redirect.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secrets-env -->
### sec-secrets-env — Load secrets from the environment

The Flask secret key comes from `FLASK_SECRET_KEY`; never commit a session key, and rotate any key that was ever in git history.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-http-headers -->
### sec-http-headers — Keep CORS and CSP strict

CORS origins come from the `CORS_ALLOWED_ORIGINS` allowlist (never `*`) and the CSP uses `script-src 'self'` without `unsafe-inline`; keep scripts in external files.
<!-- /harness-remediation -->
