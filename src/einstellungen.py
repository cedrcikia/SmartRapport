# einstellungen.py · Person A · Stundenlohn, Sollzeit, Zuschlag, Abzüge
# (US-01 bis US-03). Liest, speichert und ändert einstellungen.txt.

from pathlib import Path

from src.hilfen import ist_dezimalzahl, ist_nur_ziffern
from src.pfade import EINSTELLUNGEN_DATEI

STANDARD_EINSTELLUNGEN = {
    "stundenlohn": 30.0,
    "soll_min": 480,
    "zuschlag": 25.0,
    "ahv": 5.3,
    "alv": 1.1,
    "nbu": 3.74,
}

# Diese Werte sind Prozente und stehen ohne unnötiges ".0" in der Datei
PROZENT_SCHLUESSEL = ("zuschlag", "ahv", "alv", "nbu")


def lade_einstellungen(dateiname=EINSTELLUNGEN_DATEI):
    """US-01: Liest die Einstellungen. Fehlt die Datei, gelten die
    Standardwerte und die Datei wird angelegt.
    """
    if not Path(dateiname).exists():
        speichere_einstellungen(STANDARD_EINSTELLUNGEN, dateiname)
        return dict(STANDARD_EINSTELLUNGEN)
    einstellungen = dict(STANDARD_EINSTELLUNGEN)
    with open(dateiname, "r", encoding="utf-8") as datei:
        for zeile in datei:
            if "=" not in zeile:
                continue
            schluessel, wert = zeile.strip().split("=", 1)
            # Kaputte Werte überspringen, dann gilt der Standardwert
            if not ist_dezimalzahl(wert):
                continue
            if schluessel == "soll_min":
                einstellungen[schluessel] = int(float(wert))
            else:
                einstellungen[schluessel] = float(wert)
    return einstellungen


def speichere_einstellungen(einstellungen, dateiname=EINSTELLUNGEN_DATEI):
    """Schreibt jedes Paar als Zeile schluessel=wert in die Datei."""
    with open(dateiname, "w", encoding="utf-8") as datei:
        for schluessel, wert in einstellungen.items():
            if schluessel == "stundenlohn":
                datei.write(f"{schluessel}={wert:.2f}\n")
            elif schluessel in PROZENT_SCHLUESSEL:
                datei.write(f"{schluessel}={wert:g}\n")
            else:
                datei.write(f"{schluessel}={wert}\n")


def aendere_stundenlohn(einstellungen):
    """US-01: fragt, bis der Lohn gültig ist, speichert und bestätigt."""
    eingabe = input("Stundenlohn: ")
    while not ist_dezimalzahl(eingabe) or float(eingabe) <= 0:
        print("Ungültiger Stundenlohn.")
        eingabe = input("Stundenlohn: ")
    betrag = float(eingabe)
    einstellungen["stundenlohn"] = betrag
    speichere_einstellungen(einstellungen)
    print(f"Stundenlohn gespeichert: CHF {betrag:.2f}")


def aendere_sollzeit(einstellungen):
    """US-02: fragt Stunden und Minuten pro Tag, speichert in Minuten."""
    eingabe = input("Stunden: ")
    while (not ist_nur_ziffern(eingabe)
           or int(eingabe) < 1 or int(eingabe) > 24):
        print("Ungültige Eingabe.")
        eingabe = input("Stunden: ")
    stunden = int(eingabe)

    eingabe = input("Minuten: ")
    while (not ist_nur_ziffern(eingabe) or int(eingabe) > 59
           or (stunden == 24 and int(eingabe) > 0)):
        print("Ungültige Eingabe.")
        eingabe = input("Minuten: ")
    minuten = int(eingabe)

    einstellungen["soll_min"] = stunden * 60 + minuten
    speichere_einstellungen(einstellungen)
    print(f"Sollzeit gespeichert: {stunden} Std {minuten:02d} Min pro Tag")


def frage_prozent(frage):
    """Fragt einen Prozentwert von 0 bis 100, bis er gültig ist."""
    eingabe = input(frage)
    while not ist_dezimalzahl(eingabe) or float(eingabe) > 100:
        print("Ungültiger Prozentwert (0 bis 100).")
        eingabe = input(frage)
    return float(eingabe)


def aendere_zuschlag_und_abzuege(einstellungen):
    """US-03: fragt Zuschlag, AHV, ALV und NBU, speichert und bestätigt."""
    print("[EINSTELLUNGEN - ZUSCHLAG UND ABZÜGE]")
    einstellungen["zuschlag"] = frage_prozent("Überstunden-Zuschlag in %: ")
    einstellungen["ahv"] = frage_prozent("AHV-Abzug in %: ")
    einstellungen["alv"] = frage_prozent("ALV-Abzug in %: ")
    einstellungen["nbu"] = frage_prozent("NBU-Abzug in %: ")
    speichere_einstellungen(einstellungen)
    print("Sätze gespeichert")
