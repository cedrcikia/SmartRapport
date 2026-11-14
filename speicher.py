# speicher.py · Person C · US-06 Einträge speichern und laden

from pathlib import Path

DATEINAME = "stunden.txt"


def nur_ziffern(text):
    """DUMMY: True, wenn der Text nicht leer ist und nur Ziffern hat."""
    if len(text) == 0:
        return False
    for zeichen in text:
        if zeichen not in "0123456789":
            return False
    return True


def ist_gueltige_uhrzeit(text):
    """DUMMY: True bei einer Uhrzeit HH:MM von 00:00 bis 23:59."""
    if len(text) != 5 or text[2] != ":":
        return False
    if not nur_ziffern(text[0:2]) or not nur_ziffern(text[3:5]):
        return False
    return int(text[0:2]) <= 23 and int(text[3:5]) <= 59


def ist_gueltiges_datum(text):
    """DUMMY: True bei einem Datum im Format TT.MM.JJJJ.

    Prüft nur das Format, nicht ob es den Tag gibt (z. B. 31.02.).
    Das macht die richtige Version von Cédric.
    """
    if len(text) != 10 or text[2] != "." or text[5] != ".":
        return False
    tag = text[0:2]
    monat = text[3:5]
    jahr = text[6:10]
    if not nur_ziffern(tag) or not nur_ziffern(monat):
        return False
    if not nur_ziffern(jahr):
        return False
    return 1 <= int(tag) <= 31 and 1 <= int(monat) <= 12


def zeit_zu_minuten(text):
    """DUMMY: Wandelt "07:30" in Minuten um (450)."""
    return int(text[0:2]) * 60 + int(text[3:5])


def datum_existiert(eintraege, datum):
    """DUMMY: True, wenn es für dieses Datum schon einen Eintrag gibt."""
    for eintrag in eintraege:
        if eintrag["datum"] == datum:
            return True
    return False


def eintrag_zu_zeile(eintrag):
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

    start_min = zeit_zu_minuten(start)
    ende_min = zeit_zu_minuten(ende)
    if ende_min <= start_min:
        return False

    # Pause zuerst als Text prüfen, damit "abc" oder "4.5" nicht
    # bei int() abstürzt
    if not nur_ziffern(pause_text):
        return False
    if int(pause_text) >= ende_min - start_min:
        return False
    return True


def speichere_eintraege(eintraege, dateiname=DATEINAME):
    # "w" ersetzt den alten Inhalt, weil immer die ganze Liste
    # geschrieben wird (auch nach Ändern oder Löschen)
    with open(dateiname, "w", encoding="utf-8") as datei:
        for eintrag in eintraege:
            datei.write(eintrag_zu_zeile(eintrag) + "\n")


def lade_eintraege(dateiname=DATEINAME):
    eintraege = []
    # Fehlt die Datei, startet die App mit einer leeren Liste
    if not Path(dateiname).exists():
        return eintraege

    with open(dateiname, "r", encoding="utf-8") as datei:
        nummer = 0
        for zeile in datei:
            nummer += 1
            # Zeilenumbruch \n am Ende entfernen
            zeile = zeile.strip()
            # Leere Zeilen still überspringen (z. B. am Dateiende)
            if zeile == "":
                continue
            felder = zeile.split(";")
            if not ist_gueltige_zeile(felder):
                print(f"Zeile {nummer} übersprungen: {zeile}")
                continue
            if datum_existiert(eintraege, felder[0]):
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
