import os

from flask import request

from flask_webgoat import create_app

app = create_app()

# Comma-separated list of exact origins allowed for cross-origin requests.
# Default is empty: no CORS header is sent (same-origin only).
ALLOWED_CORS_ORIGINS = frozenset(
    origin.strip()
    for origin in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip() and origin.strip() != '*'
)

@app.after_request
def add_csp_headers(response):
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_CORS_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers.add('Vary', 'Origin')
    response.headers['Content-Security-Policy'] = "script-src 'self'"
    return response

if __name__ == '__main__':
    app.run()
