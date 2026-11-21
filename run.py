import os

from flask import request
from flask_webgoat import create_app

app = create_app()


def _allowed_cors_origins():
    # Comma-separated list of exact origins, e.g. "https://app.example.com".
    # Empty/unset means no cross-origin access is granted.
    raw = os.environ.get('CORS_ALLOWED_ORIGINS', '')
    return {o.strip() for o in raw.split(',') if o.strip() and o.strip() != '*'}


@app.after_request
def add_csp_headers(response):
    # vulnerability: Broken Access Control
    # Same-origin by default; cross-origin only for explicitly allowlisted origins.
    origin = request.headers.get('Origin')
    if origin and origin in _allowed_cors_origins():
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers.add('Vary', 'Origin')
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self'"
    return response

if __name__ == '__main__':
    app.run()
