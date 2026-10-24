from flask_webgoat import create_app

app = create_app()

@app.after_request
def add_csp_headers(response):
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self'; object-src 'none'; base-uri 'self'"
    return response

if __name__ == '__main__':
    app.run()
