# erfassung.py · Person B · Arbeitstag und Pause erfassen (US-04, US-05)

from src.hilfen import (berechne_arbeitszeit_min, hat_eintrag_fuer_datum,
                        ist_gueltige_uhrzeit, ist_gueltiges_datum,
                        ist_nur_ziffern, lies_eingabe,
                        wandle_minuten_in_text_um,
                        wandle_zeit_in_minuten_um)
from src.speicher import speichere_eintraege


def frage_datum(eintraege):
    """US-04: fragt ein Datum, bis es gültig ist und noch frei ist."""
    while True:
        datum = lies_eingabe("Datum (TT.MM.JJJJ): ")
        if not ist_gueltiges_datum(datum):
            print("Ungültiges Datum (TT.MM.JJJJ).")
        elif hat_eintrag_fuer_datum(eintraege, datum):
            # pro Datum höchstens ein Eintrag (Festlegung 2)
            print("Für dieses Datum gibt es schon einen Eintrag.")
        else:
            return datum


def frage_uhrzeit(frage):
    """US-04: fragt eine Uhrzeit, bis sie gültig ist."""
    while True:
        uhrzeit = lies_eingabe(frage)
        if ist_gueltige_uhrzeit(uhrzeit):
            return uhrzeit
        print("Ungültige Uhrzeit (HH:MM).")


def frage_pause(max_min):
    """US-05: fragt die Pause, sie muss kürzer als max_min sein."""
    while True:
        eingabe = lies_eingabe("Pause in Minuten: ")
        # nur ganze Zahlen erlaubt: leer, -5, 4.5 und abc fallen weg
        if not ist_nur_ziffern(eingabe):
            print("Ungültige Pause.")
        elif int(eingabe) >= max_min:
            print("Die Pause muss kürzer sein als die Zeit zwischen "
                  "Start und Ende.")
        else:
            # int() erst hier: ungültige Eingaben kommen nicht so weit
            return int(eingabe)


def frage_eintrag(eintraege):
    """US-04 und US-05: fragt Datum, Start, Ende und Pause und gibt den
    neuen Eintrag zurück. Wird auch beim Ändern (US-08) gebraucht.
    """
    datum = frage_datum(eintraege)
    start = frage_uhrzeit("Start (HH:MM): ")
    ende = frage_uhrzeit("Ende (HH:MM): ")

    # Ende muss am selben Tag nach dem Start liegen, sonst nur Ende neu
    start_min = wandle_zeit_in_minuten_um(start)
    while wandle_zeit_in_minuten_um(ende) <= start_min:
        print("Das Ende muss nach dem Start liegen.")
        ende = frage_uhrzeit("Ende (HH:MM): ")

    # die Pause muss kürzer sein als die Zeit zwischen Start und Ende
    max_min = wandle_zeit_in_minuten_um(ende) - start_min
    pause = frage_pause(max_min)

    # Eintrag als Dictionary (pause_min ist int, der Rest Text)
    return {"datum": datum, "start": start, "ende": ende,
            "pause_min": pause}


def trage_arbeitstag_ein(eintraege):
    """US-04 und US-05: fragt alles, hängt den Eintrag an, speichert."""
    eintrag = frage_eintrag(eintraege)
    arbeits_min = berechne_arbeitszeit_min(eintrag)
    print(f"Arbeitszeit: {wandle_minuten_in_text_um(arbeits_min)}")

    # an die Liste anhängen und sofort speichern (US-06)
    eintraege.append(eintrag)
    if speichere_eintraege(eintraege):
        print("Eintrag gespeichert")
