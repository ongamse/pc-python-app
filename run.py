import os

from flask import request

from flask_webgoat import create_app

app = create_app()


def _allowed_origins():
    raw = os.environ.get('CORS_ALLOWED_ORIGINS', '')
    return {o.strip() for o in raw.split(',') if o.strip() and o.strip() != '*'}


@app.after_request
def add_csp_headers(response):
    # CORS: only echo back origins explicitly allowlisted via env var;
    # otherwise emit no Access-Control-Allow-Origin header (same-origin only).
    origin = request.headers.get('Origin')
    if origin and origin in _allowed_origins():
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers.add('Vary', 'Origin')
    response.headers['Content-Security-Policy'] = "script-src 'self'"
    return response

if __name__ == '__main__':
    app.run()
