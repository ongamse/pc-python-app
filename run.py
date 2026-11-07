import os

from flask import request
from flask_webgoat import create_app

app = create_app()

@app.after_request
def add_csp_headers(response):
    # CORS: no cross-origin access by default; only origins explicitly listed
    # (comma-separated) in CORS_ALLOWED_ORIGINS are echoed back.
    allowed_origins = {
        o.strip() for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
        if o.strip() and o.strip() != '*'
    }
    origin = request.headers.get('Origin')
    if origin and origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.vary.add('Origin')
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline'"
    return response

if __name__ == '__main__':
    app.run()
