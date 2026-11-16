# verwaltung.py · Person C · Einträge anzeigen, ändern, löschen (US-07, US-08)

from src.erfassung import frage_eintrag
from src.hilfen import (berechne_arbeitszeit_min, filtere_eintraege_nach_monat,
                        frage_ja_nein, frage_monat, wandle_minuten_in_text_um)
from src.speicher import speichere_eintraege


def zeige_liste(monats_eintraege):
    """Zeigt die Einträge nummeriert ab 1 und darunter das Total.
    monats_eintraege: Liste der Einträge eines Monats (nicht leer).
    Wird von zeige_eintraege (US-07) und aendere_oder_loesche_eintrag
    (US-08) gebraucht.
    """
    nummer = 0
    total_min = 0
    for eintrag in monats_eintraege:
        nummer += 1
        arbeits_min = berechne_arbeitszeit_min(eintrag)
        dauer_text = wandle_minuten_in_text_um(arbeits_min)
        print(f"{nummer}. {eintrag['datum']}  {eintrag['start']}–"
              f"{eintrag['ende']}  Pause {eintrag['pause_min']} Min  "
              f"{dauer_text}")
        total_min += arbeits_min
    print(f"Total: {wandle_minuten_in_text_um(total_min)}")


def zeige_eintraege(eintraege):
    """US-07: fragt den Monat ab und zeigt die Einträge dieses Monats."""
    monat = frage_monat()
    monats_eintraege = filtere_eintraege_nach_monat(eintraege, monat)
    if len(monats_eintraege) == 0:
        print(f"Keine Einträge für {monat}.")
    else:
        zeige_liste(monats_eintraege)


def waehle_eintrag(monats_eintraege):
    """Fragt die Nummer, bis sie in der Liste vorkommt, und gibt den
    gewählten Eintrag zurück (Nummer 1 ist Index 0).
    """
    # Gültige Nummern als Text sammeln ("1", "2", ...), damit eine
    # Eingabe wie "abc" nicht zum Absturz führt
    gueltige_nummern = []
    for nummer in range(1, len(monats_eintraege) + 1):
        gueltige_nummern.append(str(nummer))

    eingabe = input("Nummer: ")
    while eingabe not in gueltige_nummern:
        print("Ungültige Nummer.")
        eingabe = input("Nummer: ")
    return monats_eintraege[int(eingabe) - 1]


def aendere_eintrag(eintraege, eintrag):
    """US-08: ersetzt den Eintrag durch neu abgefragte Werte und speichert."""
    # Alten Eintrag zuerst herausnehmen, damit sein Datum wieder frei ist
    eintraege.remove(eintrag)
    neuer_eintrag = frage_eintrag(eintraege)
    eintraege.append(neuer_eintrag)
    speichere_eintraege(eintraege)


def loesche_eintrag(eintraege, eintrag):
    """US-08: löscht den Eintrag nach Rückfrage und speichert."""
    if frage_ja_nein("Wirklich löschen? (j/n)"):
        eintraege.remove(eintrag)
        speichere_eintraege(eintraege)


def aendere_oder_loesche_eintrag(eintraege):
    """US-08: Eintrag eines Monats über seine Nummer wählen, danach
    ändern (1) oder löschen (2).
    """
    monat = frage_monat()
    monats_eintraege = filtere_eintraege_nach_monat(eintraege, monat)
    if len(monats_eintraege) == 0:
        print(f"Keine Einträge für {monat}.")
        return

    zeige_liste(monats_eintraege)
    eintrag = waehle_eintrag(monats_eintraege)

    wahl = input("1 = ändern, 2 = löschen: ")
    while wahl != "1" and wahl != "2":
        print("Ungültige Wahl.")
        wahl = input("1 = ändern, 2 = löschen: ")

    if wahl == "1":
        aendere_eintrag(eintraege, eintrag)
    else:
        loesche_eintrag(eintraege, eintrag)
