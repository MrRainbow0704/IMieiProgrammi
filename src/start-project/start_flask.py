from sys import exit as sys_exit
from pathlib import Path


def start_flask(ROOT_DIR: Path, APP_NAME: str) -> None:
    try:
        dirs = ["app", "templates", "static", "static/css", "static/js", "static/img"]
        files = {
            "config.py": f"""from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 80
DEBUG = True
""",
            "run.py": f"""import app
import config


app.app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
""",
            "app/__init__.py": f"""from flask import Flask
import config


app = Flask(__name__, root_path=config.ROOT_DIR)

from . import routes
""",
            "app/routes.py": f"""from flask import render_template
from . import app


@app.route("/")
def index():
    return render_template("index.html")
""",
            "templates/base.html": f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{{{url_for('static', filename='css/styles.css')}}}}">
    <title>{{% block title %}}{APP_NAME}{{% endblock title %}}</title>
</head>
<body>
    <header>
        {{% block header %}}
        <h1>{APP_NAME}</h1>
        {{% endblock header %}}
    </header>
    <main>
        {{% block main %}}
        {{% endblock main %}}
    </main>
    <footer>
        {{% block footer %}}
        <p>&COPY; Your Name YEAR</p>
        {{% endblock footer %}}
    </footer>
    <script src="{{{{url_for('static', filename='js/script.js')}}}}"></script>
</body>
</html>
""",
            "templates/index.html": """{% extends "base.html" %}

{% block main %}
<h2>Index</h2>
{% endblock main %}
""",
            "static/css/styles.css": """html, body {
    padding: 0;
    margin: 0;
}

header {
    margin: 0 auto;
    text-align: center;
}

main {
    margin: 5px;
    padding: 5px;
}

footer {
    margin: 0 auto;
    text-align: center;
}
""",
            "static/js/script.js": "",
        }
        
        for d in dirs:
            (ROOT_DIR / d).mkdir(exist_ok=True, parents=True)
        for p, f in files.items():
            with open(ROOT_DIR / p, "w") as file:
                file.write(f)
    except Exception as e:
        sys_exit(
            "C'è stato un errore durante l'esecuzione del programma. Assicurati di avere i permessi necessari.\nErrore: "
            + e
        )
