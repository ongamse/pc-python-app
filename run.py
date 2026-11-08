import os

from flask import request
from flask_webgoat import create_app

app = create_app()

# Comma-separated list of trusted origins allowed to make cross-origin requests
# (e.g. "https://app.example.com,https://admin.example.com"). Empty by default,
# meaning same-origin only (no CORS headers are emitted).
ALLOWED_CORS_ORIGINS = frozenset(
    origin.strip().rstrip('/')
    for origin in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip() and origin.strip() != '*'
)

@app.after_request
def add_csp_headers(response):
    # Only echo back an exact-match, allowlisted origin; never a wildcard, and
    # never advertise Access-Control-Allow-Credentials.
    response.headers.add('Vary', 'Origin')
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_CORS_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    # Strict CSP: no inline or eval'd scripts; templates contain no inline
    # <script>, event-handler attributes, or inline styles.
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; "
        "base-uri 'self'; frame-ancestors 'none'"
    )
    return response

if __name__ == '__main__':
    app.run()
