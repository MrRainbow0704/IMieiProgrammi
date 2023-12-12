# start-project

`start-project` è uno strumento da riga di comando scritto in python che aiuta a creare un template per una applicazione.
Applicazioni disponibili: Flask, PHP.

Per compilare il programma, usare i seguenti comandi:
```console
pip install -U pyinstaller
pyinstaller --onefile main.py start_flask.py start_php.py
```

Per informazioni sull'uso del comando usa `start-project -h`
```console
Possibili tag del comando:
    -h | -help => Mostra questa schermata.
    -t | -type => Decidi il tipo di progetto da iniziare. I valori possibili sono: "FLASK" e "PHP".
    -n | -name => Nome da dare alla nuova cartella/applicazione. (Usare una stringa vuota o non inserire il tag per usare la cartella corrente)
```