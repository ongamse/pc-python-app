# Security

Security rules for this repository. Marked blocks are maintained by Harness remediation. Text outside those blocks is left as written.


<!-- harness-remediation:sec-sql-bind -->
### sec-sql-bind — Bind SQL parameters

Pass user data through the args parameter of query_db (? placeholders), never format it into the query string. Cast typed values such as access_level before the query.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-path-containment -->
### sec-path-containment — Contain user-named files

Run user-supplied filenames through werkzeug.utils.secure_filename and require the resolved path to sit inside the per-user data directory before writing.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-no-shell -->
### sec-no-shell — No shell for request data

Use subprocess argv lists with shell=False and validate request values against a strict allowlist; do filtering in Python rather than in a shell pipeline.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-deserialize -->
### sec-safe-deserialize — No pickle on request data

Parse request payloads with json.loads plus validation; never use pickle or yaml.load on untrusted input.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-secret-env -->
### sec-secret-env — Keep secrets out of source

Load the Flask secret key from FLASK_SECRET_KEY instead of committing it. Rotate any key that was committed, since it remains in git history.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-safe-redirect -->
### sec-safe-redirect — Route redirects through the helper

Send any user-controlled redirect target through _safe_redirect_target in auth.py, which allows only same-site relative paths.
<!-- /harness-remediation -->

<!-- harness-remediation:sec-http-headers -->
### sec-http-headers — Strict CORS and CSP

Add trusted origins through CORS_ALLOWED_ORIGINS, never '*'. Keep scripts in external files served from self so the CSP does not need unsafe-inline.
<!-- /harness-remediation -->
