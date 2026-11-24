import os

from flask import request
from flask_webgoat import create_app

app = create_app()

# Comma-separated list of exact origins allowed for cross-origin requests.
ALLOWED_CORS_ORIGINS = frozenset(
    o.strip() for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if o.strip()
)

@app.after_request
def add_csp_headers(response):
    # vulnerability: Broken Access Control
    # Same-origin by default; cross-origin only for explicitly allowlisted origins.
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_CORS_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers.add('Vary', 'Origin')
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self'"
    return response

if __name__ == '__main__':
    app.run()
