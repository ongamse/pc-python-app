# flask-webgoat

flask-webgoat is a deliberately-vulnerable application written with the Flask
web framework.

```
                                                (_(
                                                /_/'_____/)
                                                "  |      |
                                                   |""""""|
███████╗██╗      █████╗ ███████╗██╗  ██╗    ██╗    ██╗███████╗██████╗  ██████╗  ██████╗  █████╗ ████████╗
██╔════╝██║     ██╔══██╗██╔════╝██║ ██╔╝    ██║    ██║██╔════╝██╔══██╗██╔════╝ ██╔═══██╗██╔══██╗╚══██╔══╝
█████╗  ██║     ███████║███████╗█████╔╝     ██║ █╗ ██║█████╗  ██████╔╝██║  ███╗██║   ██║███████║   ██║
██╔══╝  ██║     ██╔══██║╚════██║██╔═██╗     ██║███╗██║██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══██║   ██║
██║     ███████╗██║  ██║███████║██║  ██╗    ╚███╔███╔╝███████╗██████╔╝╚██████╔╝╚██████╔╝██║  ██║   ██║
╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝
```

### Run

```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" FLASK_APP=run.py flask run
```

`FLASK_SECRET_KEY` is used to sign session cookies. If unset, a random
ephemeral key is generated at startup (sessions are invalidated on restart).

`CORS_ALLOWED_ORIGINS` is an optional comma-separated allowlist of origins
(e.g. `https://app.example.com,https://admin.example.com`) permitted to make
cross-origin requests. If unset, no `Access-Control-Allow-Origin` header is
sent (same-origin only). A wildcard (`*`) entry is ignored.

### Vulnerabilities

This project contains the following vulnerabilities:

- Remote Code Execution
- SQL injection
- XSS
- Insecure Deserialization
- Directory Traversal
- Open Redirect
- Sensitive Data Exposure
- Broken Access Control
- Security Misconfiguration

You can find each one in the codebase by grepping for the string
`vulnerability`:

```
$ grep vulnerability . -R -n | grep -v README
./flask_webgoat/actions.py:43:    # vulnerability: Remote Code Execution
./flask_webgoat/users.py:37:    # vulnerability: SQL Injection
./flask_webgoat/auth.py:17:    # vulnerability: SQL Injection
./flask_webgoat/ui.py:14:        # vulnerability: XSS
./flask_webgoat/actions.py:60:    # vulnerability: Insecure Deserialization
./flask_webgoat/actions.py:35:        # vulnerability: Directory Traversal
./flask_webgoat/auth.py:45:        # vulnerability: Open Redirect
./flask_webgoat/__init__.py:12:        # vulnerability: Sensitive Data Exposure
./run.py:23:    # vulnerability: Security Misconfiguration
```
