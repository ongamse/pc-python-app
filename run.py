import os

from flask import request
from flask_webgoat import create_app

app = create_app()


def _allowed_origins():
    # Comma-separated explicit origins, e.g. "https://app.example.com".
    # Empty by default: same-origin only (no CORS header emitted).
    raw = os.environ.get('CORS_ALLOWED_ORIGINS', '')
    return {o.strip() for o in raw.split(',') if o.strip() and o.strip() != '*'}


@app.after_request
def add_csp_headers(response):
    origin = request.headers.get('Origin')
    if origin and origin in _allowed_origins():
        response.headers['Access-Control-Allow-Origin'] = origin
    response.vary.add('Origin')
    # Scripts only from same origin: no 'unsafe-inline' / 'unsafe-eval'.
    response.headers['Content-Security-Policy'] = "script-src 'self'"
    return response

if __name__ == '__main__':
    app.run()
