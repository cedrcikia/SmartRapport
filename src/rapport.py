# rapport.py · Person D · Rapport als Textdatei speichern (US-12)

from src.berechnung import baue_uebersicht_zeilen, berechne_monat
from src.hilfen import (baue_rapport_dateiname, baue_rapport_pfad,
                        berechne_abgabetermin, berechne_arbeitszeit_min,
                        filtere_eintraege_nach_monat, frage_ja_nein,
                        frage_monat, wandle_minuten_in_text_um)

TRENNLINIE = "-" * 40


def baue_eintragszeilen(monats_eintraege):
    """Eine Zeile pro Eintrag (ab 1 nummeriert), am Schluss das Total."""
    zeilen = []
    nummer = 0
    total_min = 0
    for eintrag in monats_eintraege:
        nummer += 1
        arbeits_min = berechne_arbeitszeit_min(eintrag)
        total_min += arbeits_min
        zeilen.append(f"{nummer}. {eintrag['datum']}  {eintrag['start']}–"
                      f"{eintrag['ende']}  Pause {eintrag['pause_min']} Min  "
                      f"{wandle_minuten_in_text_um(arbeits_min)}")
    zeilen.append(f"Total: {wandle_minuten_in_text_um(total_min)}")
    return zeilen


def baue_rapport(monat, monats_eintraege, einstellungen):
    """Setzt alle Zeilen des Rapports zusammen, noch ohne Datei."""
    ergebnis = berechne_monat(monats_eintraege, einstellungen)
    zeilen = [f"SMARTRAPPORT – RAPPORT {monat}",
              f"Abgabetermin: {berechne_abgabetermin(monat)}",
              TRENNLINIE]
    zeilen += baue_eintragszeilen(monats_eintraege)
    zeilen.append(TRENNLINIE)
    zeilen += baue_uebersicht_zeilen(ergebnis, einstellungen)
    return zeilen


def speichere_rapport(eintraege, einstellungen):
    """US-12: Fragt den Monat ab und speichert den Rapport als Textdatei."""
    monat = frage_monat()
    monats_eintraege = filtere_eintraege_nach_monat(eintraege, monat)
    # Ohne Einträge gibt es keinen Rapport
    if len(monats_eintraege) == 0:
        print("Keine Einträge – Rapport nicht erstellt.")
        return
    pfad = baue_rapport_pfad(monat)
    # Bestehende Datei nur nach Rückfrage überschreiben
    if pfad.exists():
        if not frage_ja_nein("Datei existiert bereits. Überschreiben? (j/n)"):
            print("Rapport nicht gespeichert.")
            return
    zeilen = baue_rapport(monat, monats_eintraege, einstellungen)
    with open(pfad, "w", encoding="utf-8") as datei:
        for zeile in zeilen:
            datei.write(zeile + "\n")
    print(f"Rapport gespeichert als {baue_rapport_dateiname(monat)}")
