import os

from flask import request
from flask_webgoat import create_app

app = create_app()

# Explicit CORS allowlist (comma-separated origins). Empty by default: no CORS header (same-origin only).
ALLOWED_ORIGINS = frozenset(
    origin.strip()
    for origin in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip() and origin.strip() != '*'
)

@app.after_request
def add_csp_headers(response):
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.vary.add('Origin')
    response.headers['Content-Security-Policy'] = "script-src 'self'; object-src 'none'; base-uri 'self'"
    return response

if __name__ == '__main__':
    app.run()
