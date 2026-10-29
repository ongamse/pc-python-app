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
export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
FLASK_APP=run.py flask run
```

`FLASK_SECRET_KEY` is required; the app refuses to start without it.

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
./run.py:7:    # vulnerability: Broken Access Control
./run.py:9:    # vulnerability: Security Misconfiguration
```
