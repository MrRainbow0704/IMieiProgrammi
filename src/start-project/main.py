print("Programma creato da Marco Simone. Tutti i diritti riservati.")

from sys import exit as sys_exit

try:
    from sys import argv
    from os import getcwd
    from pathlib import Path
except Exception as e:
    sys_exit(
        f"C'è stato un errore durante l'importazione delle libreie. Assicurati di aver installato le librerie os e Pathlib.\nErrore: {e}"
    )


# Prendi la work dir
WORK_DIR = Path(getcwd())

HELP_TEXT = """Questa è la sezione "aiuto" del comando.
Possibili tag del comando:
    -h | -help => Mostra questa schermata.
    -t | -type => Decidi il tipo di progetto da iniziare. I valori possibili sono: "FLASK" e "PHP".
    -n | -name => Nome da dare alla nuova cartella/applicazione. (Usare una stringa vuota o non inserire il tag per usare la cartella corrente)
"""
tags = ("-h", "-help", "-t", "-type", "-n", "-name")

# Gestione degli argv
if len(argv) == 1 or argv[1] in ("-h", "-help"):
    sys_exit(HELP_TEXT)
else:
    # Controlla tag duplicati
    for t in tags:
        if argv.count(t) > 1:
            sys_exit(f"Troppi tag '{t}'.")

    # Prendi il valore del tag -t | -type
    try:
        if argv.count("-t"):
            t = argv.index("-t")
        else:
            t = argv.index("-type")
        APP_TYPE = argv[t + 1].upper()
        if APP_TYPE.startswith("-"):
            sys_exit(f"{APP_TYPE} non è un tipo valido di applicazione.")
    except (ValueError, IndexError):
        sys_exit("Non è stato specificato un tipo di applicazione")

    # Prendi il valore del tag -n | -name
    try:
        if argv.count("-n"):
            n = argv.index("-n")
        else:
            n = argv.index("-name")
        APP_NAME = argv[n + 1]
        if APP_NAME.startswith("-"):
            sys_exit(f"{APP_NAME} non è un nome valido per l'applicazione.")
    except (ValueError, IndexError):
        APP_NAME = ""

    # Crea i file nella directory principale
    ROOT_DIR = WORK_DIR / APP_NAME
    ROOT_DIR.mkdir(parents=True, exist_ok=True)

    # Dai un nome template all'applicazone se non ne è stato provveduto uno
    if not APP_NAME:
        APP_NAME = "My App"

    if APP_TYPE == "PHP":
        from start_php import start_php

        start_php(ROOT_DIR, APP_NAME)
    elif APP_TYPE == "FLASK":
        from start_flask import start_flask

        start_flask(ROOT_DIR, APP_NAME)

    else:
        sys_exit("Il tipo di progetto non è valido.")

sys_exit("Programma completato.")

