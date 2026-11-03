# einstellungen.py · Person A · US-01 Stundenlohn eingeben
# Liest, speichert und ändert die Einstellungen in einstellungen.txt.

from pathlib import Path

DATEINAME = "einstellungen.txt"
STANDARD = {"stundenlohn": 30.0, "soll_min": 480, "zuschlag": 25.0, "ahv": 5.3, "alv": 1.1, "nbu": 3.74}


def lade_einstellungen():
    """Liest einstellungen.txt. Fehlt die Datei, gelten die Standardwerte."""
    if not Path(DATEINAME).exists():
        speichere_einstellungen(STANDARD)
        return dict(STANDARD)
    einstellungen = dict(STANDARD)              # Kopie, kein Alias
    with open(DATEINAME, "r") as datei:
        for zeile in datei:
            if "=" not in zeile:  # leere Zeile
                continue
            schlüssel, wert = zeile.strip().split("=", 1)
            if not wert.replace(".", "", 1).isdecimal():  # z.B. abc
                continue
            if schlüssel == "soll_min":
                einstellungen[schlüssel] = int(float(wert))
            else:
                einstellungen[schlüssel] = float(wert)
    return einstellungen


def speichere_einstellungen(einstellungen):
    """Schreibt jedes Paar als Zeile schlüssel=wert in einstellungen.txt."""
    with open(DATEINAME, "w") as datei:
        for schlüssel, wert in einstellungen.items():
            if schlüssel == "stundenlohn":
                datei.write(f"{schlüssel}={wert:.2f}\n")
            else:
                datei.write(f"{schlüssel}={wert}\n")


def stundenlohn_eingeben(einstellungen):
    """US-01: fragt, bis der Lohn gültig ist, speichert und bestätigt."""
    text = input("Stundenlohn: ")
    while not text.replace(".", "", 1).isdecimal() or float(text) <= 0:
        print("Ungültiger Stundenlohn.")
        text = input("Stundenlohn: ")
    betrag = float(text)
    einstellungen["stundenlohn"] = betrag
    speichere_einstellungen(einstellungen)
    print(f"Stundenlohn gespeichert: CHF {betrag:.2f}")