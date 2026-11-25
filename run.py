import os

from flask import request

from flask_webgoat import create_app

app = create_app()

@app.after_request
def add_csp_headers(response):
    # CORS: no header by default (same-origin only). Reflect the request
    # Origin only when it exactly matches an explicit allowlist from the
    # CORS_ALLOWED_ORIGINS env var (comma-separated). Never use a wildcard.
    allowed_origins = {
        origin.strip()
        for origin in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
        if origin.strip() and origin.strip() != '*'
    }
    response.headers.add('Vary', 'Origin')
    origin = request.headers.get('Origin')
    if origin and origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline'"
    return response

if __name__ == '__main__':
    app.run()
