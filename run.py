import os

from flask import request

from flask_webgoat import create_app

app = create_app()


def _allowed_origins():
    # Comma-separated list of exact origins permitted for cross-origin requests.
    # Default is empty: same-origin only (no CORS headers emitted).
    raw = os.environ.get("ALLOWED_ORIGINS", "")
    return {o.strip() for o in raw.split(",") if o.strip() and o.strip() != "*"}


@app.after_request
def add_csp_headers(response):
    response.headers.add('Vary', 'Origin')
    origin = request.headers.get('Origin')
    if origin and origin in _allowed_origins():
        response.headers['Access-Control-Allow-Origin'] = origin
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline'"
    return response

if __name__ == '__main__':
    app.run()
