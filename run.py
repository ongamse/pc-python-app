from flask_webgoat import create_app

app = create_app()

@app.after_request
def add_csp_headers(response):
	def add_csp_headers(response):
	    response.headers['Access-Control-Allow-Origin'] = '*'
	    response.headers['Content-Security-Policy'] = "script-src 'self'"
	    return response

    app.run()

