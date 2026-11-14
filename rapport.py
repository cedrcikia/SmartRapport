# rapport.py · Person D · Rapport als Textdatei speichern (US-12)

import os

from berechnung import baue_uebersicht_zeilen, berechne_monat
from hilfen import (abgabetermin, arbeitszeit_minuten, eintraege_des_monats,
                    frage_ja_nein, frage_monat, minuten_zu_text,
                    rapport_dateiname)

TRENNLINIE = "-" * 40


def baue_eintragszeilen(monats_eintraege):
    """Eine Zeile pro Eintrag (ab 1 nummeriert), am Schluss das Total."""
    zeilen = []
    nummer = 0
    total = 0
    for eintrag in monats_eintraege:
        nummer += 1
        minuten = arbeitszeit_minuten(eintrag)
        total += minuten
        zeilen.append(f"{nummer}. {eintrag['datum']}  {eintrag['start']}–"
                      f"{eintrag['ende']}  Pause {eintrag['pause_min']} Min  "
                      f"{minuten_zu_text(minuten)}")
    zeilen.append(f"Total: {minuten_zu_text(total)}")
    return zeilen


def baue_rapport(monat, monats_eintraege, einstellungen):
    """Setzt alle Zeilen des Rapports zusammen, noch ohne Datei."""
    ergebnis = berechne_monat(monats_eintraege, einstellungen)
    zeilen = [f"SMARTRAPPORT – RAPPORT {monat}",
              f"Abgabetermin: {abgabetermin(monat)}",
              TRENNLINIE]
    zeilen += baue_eintragszeilen(monats_eintraege)
    zeilen.append(TRENNLINIE)
    zeilen += baue_uebersicht_zeilen(ergebnis, einstellungen)
    return zeilen


def rapport_speichern(eintraege, einstellungen):
    """US-12: Fragt den Monat ab und speichert den Rapport als Textdatei."""
    monat = frage_monat()
    monats_eintraege = eintraege_des_monats(eintraege, monat)
    # Ohne Einträge gibt es keinen Rapport
    if len(monats_eintraege) == 0:
        print("Keine Einträge – Rapport nicht erstellt.")
        return
    dateiname = rapport_dateiname(monat)
    # Bestehende Datei nur nach Rückfrage überschreiben
    if os.path.exists(dateiname):
        if not frage_ja_nein("Datei existiert bereits. Überschreiben? (j/n)"):
            print("Rapport nicht gespeichert.")
            return
    zeilen = baue_rapport(monat, monats_eintraege, einstellungen)
    with open(dateiname, "w", encoding="utf-8") as datei:
        for zeile in zeilen:
            datei.write(zeile + "\n")
    print(f"Rapport gespeichert als {dateiname}")
