import os

from flask import request

from flask_webgoat import create_app

app = create_app()

# Comma-separated list of origins allowed for cross-origin access.
# Empty (default) means same-origin only: no CORS header is emitted.
ALLOWED_ORIGINS = frozenset(
    origin.strip()
    for origin in os.environ.get('ALLOWED_ORIGINS', '').split(',')
    if origin.strip() and origin.strip() != '*'
)

@app.after_request
def add_csp_headers(response):
    response.vary.add('Origin')
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; "
        "base-uri 'self'; frame-ancestors 'none'"
    )
    return response

if __name__ == '__main__':
    app.run()
