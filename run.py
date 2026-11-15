import os

from flask import request

from flask_webgoat import create_app

app = create_app()

# Explicit CORS origin allowlist, comma-separated (for example
# "https://app.example.com,https://admin.example.com"). Empty by default, so no
# cross-origin access is granted (same-origin only).
ALLOWED_CORS_ORIGINS = frozenset(
    origin.strip()
    for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip() and origin.strip() != "*"
)

@app.after_request
def add_csp_headers(response):
    origin = request.headers.get('Origin')
    if origin and origin in ALLOWED_CORS_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.vary.add('Origin')
    # Strict CSP: no inline scripts or eval; the templates contain no inline JS.
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; "
        "base-uri 'self'; frame-ancestors 'none'"
    )
    return response

if __name__ == '__main__':
    app.run()
