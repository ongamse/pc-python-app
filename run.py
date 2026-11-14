import os

from flask import request
from flask_webgoat import create_app

app = create_app()

# Comma-separated list of origins allowed cross-origin access.
# Empty (default) means no cross-origin access; same-origin use is unaffected.
ALLOWED_ORIGINS = frozenset(
    origin.strip()
    for origin in os.environ.get('ALLOWED_ORIGINS', '').split(',')
    if origin.strip() and origin.strip() != '*'
)

@app.after_request
def add_csp_headers(response):
    response.vary.add('Origin')
    origin = request.headers.get('Origin')
    if origin is not None and origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline'"
    return response

if __name__ == '__main__':
    app.run()
