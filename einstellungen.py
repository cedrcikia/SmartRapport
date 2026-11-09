# einstellungen.py · Person A · US-01 Stundenlohn eingeben
# Liest, speichert und ändert die Einstellungen in einstellungen.txt.

from pathlib import Path

DATEINAME = "einstellungen.txt"
STANDARD = {
    "stundenlohn": 30.0,
    "soll_min": 480,
    "zuschlag": 25.0,
    "ahv": 5.3,
    "alv": 1.1,
    "nbu": 3.74,
}


def lade_einstellungen():
    """Liest einstellungen.txt. Fehlt die Datei, gelten die Standardwerte."""
    if not Path(DATEINAME).exists():
        speichere_einstellungen(STANDARD)
        return dict(STANDARD)
    einstellungen = dict(STANDARD)             
    with open(DATEINAME, "r", encoding="utf-8") as datei:
        for zeile in datei:
            if "=" not in zeile:  
                continue
            schluessel, wert = zeile.strip().split("=", 1)
            if not wert.replace(".", "", 1).isdecimal():  
                continue
            if schluessel == "soll_min":
                einstellungen[schluessel] = int(float(wert))
            else:
                einstellungen[schluessel] = float(wert)
    return einstellungen


def speichere_einstellungen(einstellungen):
    """Schreibt jedes Paar als Zeile schluessel=wert in einstellungen.txt."""
    with open(DATEINAME, "w", encoding="utf-8") as datei:
        for schluessel, wert in einstellungen.items():
            if schluessel == "stundenlohn":
                datei.write(f"{schluessel}={wert:.2f}\n")
            else:
                datei.write(f"{schluessel}={wert}\n")


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


def sollzeit_eingeben(einstellungen):
    """US-02: fragt, bis die Sollzeit pro Tag gültig ist, speichert in Minuten, bestätigt sie."""
    text = input("Stunden: ")
    while not text.isdecimal() or int(text) < 1 or int(text) > 24:
        print("Ungültige Eingabe.")
        text = input("Stunden: ")
    stunden = int(text)

    text = input("Minuten: ")
    while not text.isdecimal() or int(text) > 59 or stunden == 24 and int(text) > 0:
        print("Ungültige Eingabe.")
        text = input("Minuten: ")
    minuten = int(text)
    einstellungen["soll_min"] = stunden * 60 + minuten
    speichere_einstellungen(einstellungen)
    print(f"Sollzeit gespeichert: {stunden} Std {minuten:02d} Min pro Tag")