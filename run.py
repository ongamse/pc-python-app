import os

from flask import request
from flask_webgoat import create_app

app = create_app()

ALLOWED_ORIGINS = frozenset(
    o.strip() for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    if o.strip() and o.strip() != '*'
)

@app.after_request
def add_csp_headers(response):
    # CORS: no ACAO header by default (same-origin only); only origins
    # explicitly listed in CORS_ALLOWED_ORIGINS (comma-separated) are echoed.
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers.add('Vary', 'Origin')
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline'"
    return response

if __name__ == '__main__':
    app.run()
