"""Script per scaricare anime da AnimeSaturn creato da Marco Simone alias MrRainbow0704.
Tutti i diritti riservati.
Versione 2.1
"""

import logging, re, requests, time
from pathlib import Path
from os import getcwd


def get_episode_links(url: str) -> list[str]:
    linkRegexp = r'<a[^>]*class=["\'][^>]*bottone-ep[^>]*["\'][^>]*[^>]*>'
    hrefRegexp = r'(?<=href=["\']).*?(?=["\'])'
    zeroEpRegexp = r"[^0-9A-Za-z\n]*ep-0[^0-9A-Za-z\n]*"

    res = requests.get(url)
    if res.ok:
        # Prendi gli url dai tag <a> estraendoli con delle RegExp
        content = res.text.replace(" ", "")
        links: list[str] = re.findall(linkRegexp, content, re.IGNORECASE)
        links: list[str] = [
            re.findall(hrefRegexp, link, re.IGNORECASE)[0] for link in links
        ]

        # Gestione del caso limite "episodio 0"
        if re.findall(zeroEpRegexp, links[0], re.IGNORECASE):
            return links
        return links.insert(0, "")
    else:
        logging.warning(
            f"Ricevuto un codice diverso da 200 OK: {res.status_code}. {res.content}"
        )
        raise ConnectionError(
            f"Ricevuto un codice diverso da 200 OK: {res.status_code}. {res.content}"
        )


def get_stream_link(url: str, i: int) -> tuple[int | str]:
    linkRegexp = r'<a[^>]*href=["\'][^>]*watch\?[^>]*["\'][^>]*>'
    hrefRegexp = r'(?<=href=["\']).*?(?=["\'])'

    res = requests.get(url)
    if res.ok:
        # Estrai gli url dai tag <a> con delle RegExp
        content = res.text.replace(" ", "")
        link = re.findall(linkRegexp, content, re.IGNORECASE)[0]
        streamLink = re.findall(hrefRegexp, link, re.IGNORECASE)[0]

        return i, streamLink
    else:
        logging.warning(
            f"Ricevuto un codice diverso da 200 OK: {res.status_code}. {res.content}"
        )
        raise ConnectionError(
            f"Ricevuto un codice diverso da 200 OK: {res.status_code}. {res.content}"
        )


def get_video_link(url: str, i: int) -> tuple[int | str]:
    sourceRegexp = r"<source[^>]*>"
    srcRegexp = r'(?<=src=["\']).*?(?=["\'])'

    res = requests.get(url)
    if res.ok:
        # Estrai gli url dal tag <source> con delle RegExp
        content = res.text.replace(" ", "")
        link = re.findall(sourceRegexp, content, re.IGNORECASE)[0]
        vidLink = re.findall(srcRegexp, link, re.IGNORECASE)[0]

        return i, vidLink
    else:
        logging.warning(
            f"Ricevuto un codice diverso da 200 OK: {res.status_code}. {res.content}"
        )
        raise ConnectionError(
            f"Ricevuto un codice diverso da 200 OK: {res.status_code}. {res.content}"
        )


def download_videos(urls: list[tuple[int | str]], path: Path, filename: str) -> None:
    # Crea una lista di stream di risposte e una di stream di scrittura di bytes
    responses = {i: requests.get(url, stream=True) for i, url in urls}
    streams = {i: responses[i].iter_content(chunk_size=1024) for i, _ in urls}
    handles = {i: open(path / f"{filename}{i}.mp4", "wb") for i, _ in urls}

    start = time.perf_counter()
    for i, _ in urls:
        logging.info(f"Iniziando download di `{filename}{i}.mp4`...")

    while streams:
        for url in list(streams.keys()):
            try:
                # Prova a prendere il prossimo chunk di dati e scriverlo nel rispettivo stream di scrittura
                chunk = next(streams[url])
                handles[url].write(chunk)
            except StopIteration:
                # Quando lo stream finisce, chiudi lo stream di scrittura e rimuovi lo stream di risposte dalla lista
                handles[url].close()
                streams.pop(url)

                tot = time.perf_counter() - start
                logging.info(
                    f"Download terminato per `{filename}{url}.mp4` in {tot:0.2f} secondi."
                )
            except Exception as e:
                logging.warning(f"Errore rilevato: {e}")
                raise Exception(e)


def split_list(lst, chunk_size):
    # Divide una lista in liste più piccole di dimensione `chunk_size` o inferiori
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def main() -> None:
    # Prendi variabili dall'utente
    ROOT = Path(getcwd())
    url = input("Inserisci il link alla pagina dell'anime: ")
    primo = int(input("Inserisci il numero del primo episodio da scaricare: "))
    ultimo = int(input("Inserisci il numero dell'ultimo episodio da scaricare: ")) + 1
    path = ROOT / input(
        f'Inserisci il percorso dove salvare i file [Vuoto per: "{ROOT}"]: '
    )
    path.mkdir(parents=True, exist_ok=True)
    filename = input("Inserisci il nome per i file: ") 
    s = time.perf_counter()
    
    # Esegui lo scraping della pagina per poi scaricare tutti i video
    episodi = get_episode_links(url)
    epLinks = [
        get_stream_link(ep, i) for i, ep in enumerate(episodi[primo:ultimo], primo)
    ]
    videoLinks = [get_video_link(ep, i) for i, ep in epLinks]
    for vidLinks in split_list(videoLinks, 3):
        download_videos(vidLinks, path, filename)

    s1 = time.perf_counter() - s
    logging.info(f"Operazione terminata in {s1:0.2f} secondi.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    print(__doc__)
    main()
