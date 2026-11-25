# verwaltung.py · Person C · Einträge anzeigen, ändern, löschen
# (US-07, US-08)

from src.erfassung import frage_eintrag
from src.hilfen import (berechne_arbeitszeit_min,
                        filtere_eintraege_nach_monat, frage_ja_nein,
                        frage_monat, lies_eingabe,
                        wandle_minuten_in_text_um)
from src.speicher import speichere_eintraege


def baue_eintragszeilen(monats_eintraege):
    """Eine Zeile pro Eintrag (ab 1 nummeriert), am Schluss das Total.
    Wird von zeige_liste (US-07, US-08) und vom Rapport (US-12)
    gebraucht, so sieht die Liste überall gleich aus.
    """
    zeilen = []
    nummer = 0
    total_min = 0
    for eintrag in monats_eintraege:
        nummer += 1
        arbeits_min = berechne_arbeitszeit_min(eintrag)
        total_min += arbeits_min
        zeilen.append(f"{nummer}. {eintrag['datum']}  "
                      f"{eintrag['start']}–{eintrag['ende']}  "
                      f"Pause {eintrag['pause_min']} Min  "
                      f"{wandle_minuten_in_text_um(arbeits_min)}")
    zeilen.append(f"Total: {wandle_minuten_in_text_um(total_min)}")
    return zeilen


def zeige_liste(monats_eintraege):
    """Zeigt die Einträge eines Monats (nicht leer) nummeriert mit
    Total.
    """
    for zeile in baue_eintragszeilen(monats_eintraege):
        print(zeile)


def zeige_eintraege(eintraege):
    """US-07: fragt den Monat und zeigt die Einträge dieses Monats."""
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

    eingabe = lies_eingabe("Nummer: ")
    while eingabe not in gueltige_nummern:
        print("Ungültige Nummer.")
        eingabe = lies_eingabe("Nummer: ")
    return monats_eintraege[int(eingabe) - 1]


def frage_aendern_oder_loeschen():
    """Fragt "1" (ändern) oder "2" (löschen), bis die Wahl passt."""
    wahl = lies_eingabe("1 = ändern, 2 = löschen: ")
    while wahl != "1" and wahl != "2":
        print("Ungültige Wahl.")
        wahl = lies_eingabe("1 = ändern, 2 = löschen: ")
    return wahl


def aendere_eintrag(eintraege, eintrag):
    """US-08: ersetzt den Eintrag durch neu abgefragte Werte."""
    # Alten Eintrag zuerst entfernen, damit sein Datum wieder frei ist
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
    if frage_aendern_oder_loeschen() == "1":
        aendere_eintrag(eintraege, eintrag)
    else:
        loesche_eintrag(eintraege, eintrag)
