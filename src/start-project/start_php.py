from sys import exit as sys_exit
from pathlib import Path


def start_php(ROOT_DIR: Path, APP_NAME: str) -> None:
    try:
        dirs = ["css", "js", "img", "includes"]
        files = {
            "index.php": """<?php
include_once 'header.php'
?>
    <main>
        <h2>Index</h2>
    </main>
<?php
include_once 'footer.php'
?>""",
            "header.php": f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/styles.css">
    <title>{APP_NAME}</title>
</head>
<body>
    <header>
        <h1>{APP_NAME}</h1>
    </header>
""",
            "footer.php": """
    <footer>
        <p>&COPY; Your Name YEAR</p>
    </footer>
    <script src="js/script.js"></script>
</body>
</html>
""",
            "css/styles.css": """html, body {
    padding: 0;
    margin: 0;
    min-height: 100%;
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
            "js/script.js": "",
            "includes/functions.inc.php": "",
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
