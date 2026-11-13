import os

from flask import request
from flask_webgoat import create_app

app = create_app()

# Comma-separated list of exact origins allowed for cross-origin requests.
# Empty by default (same-origin only).
ALLOWED_CORS_ORIGINS = frozenset(
    o.strip() for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    if o.strip() and o.strip() != '*'
)

@app.after_request
def add_csp_headers(response):
    # CORS: same-origin only unless the request Origin is explicitly allowlisted.
    response.vary.add('Origin')
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_CORS_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Content-Security-Policy'] = (
        "script-src 'self'; object-src 'none'; base-uri 'self'"
    )
    return response

if __name__ == '__main__':
    app.run()
