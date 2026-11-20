# speicher.py · Person C · US-06 Einträge speichern und laden

from src.hilfen import (hat_eintrag_fuer_datum, ist_gueltige_uhrzeit,
                        ist_gueltiges_datum, ist_nur_ziffern,
                        lese_zeilen_aus_datei, schreibe_zeilen_in_datei,
                        wandle_zeit_in_minuten_um)
from src.pfade import STUNDEN_DATEI


def wandle_eintrag_in_zeile_um(eintrag):
    """Wandelt einen Eintrag in eine Zeile für stunden.txt um.

    Story: US-06 (Teil: Processing)

    Parameter:
        eintrag (dict): Ein Eintrag mit datum, start, ende und
            pause_min, z. B. {"datum": "05.10.2026",
            "start": "07:30", "ende": "17:00", "pause_min": 45}

    Rückgabe:
        str: Zeile im Format Datum;Start;Ende;Pause,
        z. B. "05.10.2026;07:30;17:00;45"

    Wird aufgerufen von: speichere_eintraege
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
    datum = felder[0]
    start = felder[1]
    ende = felder[2]
    pause_text = felder[3]

    if not ist_gueltiges_datum(datum):
        return False
    if not ist_gueltige_uhrzeit(start) or not ist_gueltige_uhrzeit(ende):
        return False

    start_min = wandle_zeit_in_minuten_um(start)
    ende_min = wandle_zeit_in_minuten_um(ende)
    if ende_min <= start_min:
        return False

    # Pause zuerst als Text prüfen, damit "abc" oder "4.5" nicht
    # bei int() abstürzt
    if not ist_nur_ziffern(pause_text):
        return False
    if int(pause_text) >= ende_min - start_min:
        return False
    return True


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
    """Liest die Einträge aus der Datei. Kaputte Zeilen werden übersprungen
    und gemeldet.
    """
    eintraege = []
    zeilen = lese_zeilen_aus_datei(dateiname)
    # Fehlt die Datei, startet die App mit einer leeren Liste
    if zeilen is None:
        return eintraege

    nummer = 0
    for zeile in zeilen:
        nummer += 1
        # Zeilenumbruch am Ende entfernen
        zeile = zeile.strip()
        # Leere Zeilen still überspringen (z. B. am Dateiende)
        if zeile == "":
            continue
        felder = zeile.split(";")
        if not ist_gueltige_zeile(felder):
            print(f"Zeile {nummer} übersprungen: {zeile}")
            continue
        if hat_eintrag_fuer_datum(eintraege, felder[0]):
            print(f"Zeile {nummer} übersprungen: Datum doppelt")
            continue
        eintrag = {
            "datum": felder[0],
            "start": felder[1],
            "ende": felder[2],
            "pause_min": int(felder[3]),
        }
        eintraege.append(eintrag)
    return eintraege
