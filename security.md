# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass user data to query_db through its args tuple with ? placeholders; never format values into the query string.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-confine -->
### sec-path-confine — Confine user-derived file paths

Resolve the target path with pathlib and reject it unless its parent is the resolved per-user directory before opening any file.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — Keep user input out of shells

Run subprocesses with a fixed argv and shell=False, and do filtering of the output in Python instead of building a shell pipeline.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-pickle -->
### sec-no-pickle — Do not unpickle request data

Decode request payloads as JSON and validate them; never call pickle.loads on data that comes from a client.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Load secret keys from the environment

Flask's secret_key comes from FLASK_SECRET_KEY, with a random per-process fallback; never commit session keys, and rotate any key that was committed.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Redirect only to local paths

Route request-supplied redirect targets through _safe_local_url in flask_webgoat/auth.py, which accepts same-site relative paths only.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-cors-allowlist -->
### sec-cors-allowlist — Use a CORS origin allowlist

Cross-origin consumers are added to the ALLOWED_ORIGINS environment variable; never set Access-Control-Allow-Origin to a wildcard.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-csp-no-inline -->
### sec-csp-no-inline — Keep CSP free of unsafe-inline

Serve new JavaScript as static files or use a per-response nonce instead of re-adding unsafe-inline to script-src.
<!-- /harness-remediation -->
