import os

from flask import request
from flask_webgoat import create_app

app = create_app()

# Comma-separated list of explicitly allowed CORS origins (empty = same-origin only).
ALLOWED_ORIGINS = frozenset(
    o.strip() for o in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
)

@app.after_request
def add_csp_headers(response):
    # Same-origin by default; cross-origin access only for explicitly allowed origins.
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.vary.add('Origin')
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    return response

if __name__ == '__main__':
    app.run()
