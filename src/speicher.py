# speicher.py · Person C · US-06 Einträge speichern und laden

from src.hilfen import (hat_eintrag_fuer_datum, ist_gueltige_uhrzeit,
                        ist_gueltiges_datum, ist_nur_ziffern,
                        lese_zeilen_aus_datei, schreibe_zeilen_in_datei,
                        wandle_zeit_in_minuten_um)
from src.pfade import STUNDEN_DATEI


def wandle_eintrag_in_zeile_um(eintrag):
    """Wandelt einen Eintrag in eine Zeile für stunden.txt um.
    Beispiel: "05.10.2026;07:30;17:00;45" (Datum;Start;Ende;Pause)
    """
    datum = eintrag["datum"]
    start = eintrag["start"]
    ende = eintrag["ende"]
    pause = eintrag["pause_min"]
    return f"{datum};{start};{ende};{pause}"


def ist_gueltige_zeile(felder):
    """True, wenn die Felder einer Zeile gleich gültig sind wie beim
    Eintragen (US-04 und US-05).
    """
    # Zuerst die Anzahl prüfen, sonst gibt felder[3] einen IndexError
    if len(felder) != 4:
        return False
    datum, start, ende, pause_text = felder
    if not ist_gueltiges_datum(datum):
        return False
    if not ist_gueltige_uhrzeit(start) or not ist_gueltige_uhrzeit(ende):
        return False

    dauer_min = (wandle_zeit_in_minuten_um(ende)
                 - wandle_zeit_in_minuten_um(start))
    if dauer_min <= 0:
        return False

    # Pause zuerst als Text prüfen, damit "abc" oder "4.5" nicht
    # bei int() abstürzt
    if not ist_nur_ziffern(pause_text):
        return False
    return int(pause_text) < dauer_min


def wandle_zeile_in_eintrag_um(zeile, nummer, eintraege):
    """Wandelt eine Zeile aus der Datei in einen Eintrag um.
    Gibt None zurück (mit Meldung), wenn die Zeile kaputt ist oder es
    das Datum schon gibt.
    """
    felder = zeile.split(";")
    if not ist_gueltige_zeile(felder):
        print(f"Zeile {nummer} übersprungen: {zeile}")
        return None
    if hat_eintrag_fuer_datum(eintraege, felder[0]):
        print(f"Zeile {nummer} übersprungen: Datum doppelt")
        return None
    return {"datum": felder[0], "start": felder[1], "ende": felder[2],
            "pause_min": int(felder[3])}


def speichere_eintraege(eintraege, dateiname=STUNDEN_DATEI):
    """Schreibt die ganze Liste in die Datei, eine Zeile pro Eintrag.
    Gibt True zurück, wenn es geklappt hat, sonst False.
    """
    # Immer die ganze Liste, auch nach Ändern oder Löschen
    zeilen = []
    for eintrag in eintraege:
        zeilen.append(wandle_eintrag_in_zeile_um(eintrag))
    return schreibe_zeilen_in_datei(dateiname, zeilen)


def lade_eintraege(dateiname=STUNDEN_DATEI):
    """Liest die Einträge aus der Datei. Kaputte Zeilen werden
    übersprungen und gemeldet.
    """
    eintraege = []
    zeilen = lese_zeilen_aus_datei(dateiname)
    # Fehlt die Datei, startet die App mit einer leeren Liste
    if zeilen is None:
        return eintraege

    for nummer, zeile in enumerate(zeilen, 1):
        zeile = zeile.strip()
        # Leere Zeilen still überspringen (z. B. am Dateiende)
        if zeile == "":
            continue
        eintrag = wandle_zeile_in_eintrag_um(zeile, nummer, eintraege)
        if eintrag is not None:
            eintraege.append(eintrag)
    return eintraege
