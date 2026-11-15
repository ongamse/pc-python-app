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
FLASK_APP=run.py flask run
```

Set `FLASK_SECRET_KEY` to a long random value to sign sessions (for example,
`export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"`).
If it is unset, a random per-process key is generated, so sessions are
invalidated on restart and are not shared between workers.

By default no cross-origin (CORS) access is granted. To allow specific origins,
set `CORS_ALLOWED_ORIGINS` to a comma-separated list of exact origins (for
example `https://app.example.com,https://admin.example.com`). A wildcard `*`
is ignored.

### Vulnerabilities

This project contains the following vulnerabilities:

- Remote Code Execution
- SQL injection
- XSS
- Directory Traversal
- Open Redirect
- Sensitive Data Exposure
- Security Misconfiguration

You can find each one in the codebase by grepping for the string
`vulnerability`:

```
$ grep vulnerability . -R -n | grep -v README
./flask_webgoat/actions.py:43:    # vulnerability: Remote Code Execution
./flask_webgoat/users.py:37:    # vulnerability: SQL Injection
./flask_webgoat/auth.py:17:    # vulnerability: SQL Injection
./flask_webgoat/ui.py:14:        # vulnerability: XSS
./flask_webgoat/actions.py:35:        # vulnerability: Directory Traversal
./flask_webgoat/auth.py:45:        # vulnerability: Open Redirect
./flask_webgoat/__init__.py:12:        # vulnerability: Sensitive Data Exposure
```
