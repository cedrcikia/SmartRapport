# erfassen.py · Person B · Arbeitstag und Pause erfassen (US-04, US-05)

from hilfen import (arbeitszeit_minuten, datum_existiert, minuten_zu_text,
                    zeit_zu_minuten)


# DUMMY – wird später durch speichere_eintraege() aus speicher.py ersetzt (US-06)
def speichere_eintraege(eintraege):
    # Schreibt noch nichts in stunden.txt, zeigt nur, dass gespeichert würde
    print(f"(DUMMY) stunden.txt gespeichert: {len(eintraege)} Einträge")


# EIGENE VERSION – wird gelöscht, sobald hilfen.py sie hat
def ist_gueltiges_datum(text):
    # Prüft TT.MM.JJJJ und ob es das Datum wirklich gibt
    # Form: genau 10 Zeichen, Punkte an Stelle 2 und 5
    if len(text) != 10 or text[2] != "." or text[5] != ".":
        return False
    # alle anderen Zeichen müssen Ziffern sein
    for zeichen in text[0:2] + text[3:5] + text[6:10]:
        if zeichen not in "0123456789":
            return False
    # int() erst jetzt, weil nur noch Ziffern übrig sind
    tag = int(text[0:2])
    monat = int(text[3:5])
    jahr = int(text[6:10])
    if monat < 1 or monat > 12:
        return False
    # Tage pro Monat, Index 0 = Januar
    tage = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    letzter_tag = tage[monat - 1]
    # Im Schaltjahr hat der Februar 29 Tage
    if monat == 2:
        if jahr % 400 == 0 or (jahr % 4 == 0 and jahr % 100 != 0):
            letzter_tag = 29
    # z. B. 31.02.2026 fällt hier weg
    if tag < 1 or tag > letzter_tag:
        return False
    return True


# EIGENE VERSION – wird gelöscht, sobald hilfen.py sie hat
def ist_gueltige_uhrzeit(text):
    # Prüft HH:MM von 00:00 bis 23:59 (7:30 und 24:00 sind ungültig)
    if len(text) != 5 or text[2] != ":":
        return False
    for zeichen in text[0:2] + text[3:5]:
        if zeichen not in "0123456789":
            return False
    stunden = int(text[0:2])
    minuten = int(text[3:5])
    return stunden <= 23 and minuten <= 59


def frage_datum(eintraege):
    """US-04: fragt ein Datum ab, bis es gültig ist und noch frei ist."""
    while True:
        datum = input("Datum (TT.MM.JJJJ): ")
        if not ist_gueltiges_datum(datum):
            print("Ungültiges Datum (TT.MM.JJJJ).")
        elif datum_existiert(eintraege, datum):
            # pro Datum höchstens ein Eintrag (Festlegung 2)
            print("Für dieses Datum gibt es schon einen Eintrag.")
        else:
            return datum


def frage_uhrzeit(text):
    """US-04: fragt eine Uhrzeit mit dem Fragetext ab, bis sie gültig ist."""
    while True:
        zeit = input(text)
        if ist_gueltige_uhrzeit(zeit):
            return zeit
        print("Ungültige Uhrzeit (HH:MM).")


def frage_pause(max_min):
    """US-05: fragt die Pause ab, bis sie gültig und kürzer als max_min ist."""
    while True:
        pause = input("Pause in Minuten: ")

        # kein Zeichen ist leere Eingabe, deshalb separat prüfen
        gueltig = True
        if pause == "":
            gueltig = False

        # nur ganze Zahlen erlaubt; -5, 4.5 und abc fallen weg
        for zeichen in pause:
            if zeichen not in "0123456789":
                gueltig = False

        # int() erst hier: ungültige Eingaben kommen gar nicht so weit
        if gueltig == False:
            print("Ungültige Pause.")
        elif int(pause) >= max_min:
            print("Die Pause muss kürzer sein als die Zeit zwischen Start und Ende.")
        else:
            return int(pause)


def arbeitstag_eintragen(eintraege):
    """US-04 und US-05: fragt alles ab, hängt den Eintrag an und speichert."""
    datum = frage_datum(eintraege)
    start = frage_uhrzeit("Start (HH:MM): ")
    ende = frage_uhrzeit("Ende (HH:MM): ")

    # Ende muss am selben Tag nach dem Start liegen, sonst nur Ende neu fragen
    while zeit_zu_minuten(ende) <= zeit_zu_minuten(start):
        print("Das Ende muss nach dem Start liegen.")
        ende = frage_uhrzeit("Ende (HH:MM): ")

    # die Pause muss kürzer sein als die Zeit zwischen Start und Ende
    max_min = zeit_zu_minuten(ende) - zeit_zu_minuten(start)
    pause = frage_pause(max_min)

    # Eintrag als Dictionary wie im Teamplan (pause_min ist int, Rest Text)
    eintrag = {"datum": datum, "start": start, "ende": ende, "pause_min": pause}
    print(f"Arbeitszeit: {minuten_zu_text(arbeitszeit_minuten(eintrag))}")

    # an die Liste anhängen und sofort speichern (US-06)
    eintraege.append(eintrag)
    speichere_eintraege(eintraege)
