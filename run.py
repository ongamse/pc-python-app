import os

from flask import request

from flask_webgoat import create_app

app = create_app()

# Explicit allowlist of trusted cross-origin callers, comma-separated, e.g.
# CORS_ALLOWED_ORIGINS="https://app.example.com,https://admin.example.com".
# Defaults to empty: no cross-origin access (same-origin only).
ALLOWED_ORIGINS = frozenset(
    origin.strip()
    for origin in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip() and origin.strip() != '*'
)

@app.after_request
def add_csp_headers(response):
    response.vary.add('Origin')
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline'"
    return response

if __name__ == '__main__':
    app.run()
