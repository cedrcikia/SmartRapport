# rapport.py · Person D · Rapport als Textdatei speichern (US-12)

from src.berechnung import baue_uebersicht_zeilen, berechne_monat
from src.hilfen import (baue_rapport_dateiname, baue_rapport_pfad,
                        berechne_abgabetermin,
                        filtere_eintraege_nach_monat, frage_ja_nein,
                        frage_monat, schreibe_zeilen_in_datei)
from src.verwaltung import baue_eintragszeilen

TRENNLINIE_LAENGE = 40


def baue_rapport(monat, monats_eintraege, einstellungen):
    """Setzt alle Zeilen des Rapports zusammen, noch ohne Datei."""
    ergebnis = berechne_monat(monats_eintraege, einstellungen)
    trennlinie = "-" * TRENNLINIE_LAENGE
    zeilen = [f"SMARTRAPPORT – RAPPORT {monat}",
              f"Abgabetermin: {berechne_abgabetermin(monat)}",
              trennlinie]
    zeilen += baue_eintragszeilen(monats_eintraege)
    zeilen.append(trennlinie)
    zeilen += baue_uebersicht_zeilen(ergebnis, einstellungen)
    return zeilen


def speichere_rapport(eintraege, einstellungen):
    """US-12: Fragt den Monat und speichert den Rapport."""
    monat = frage_monat()
    monats_eintraege = filtere_eintraege_nach_monat(eintraege, monat)
    # Ohne Einträge gibt es keinen Rapport
    if len(monats_eintraege) == 0:
        print("Keine Einträge – Rapport nicht erstellt.")
        return
    pfad = baue_rapport_pfad(monat)
    # Bestehende Datei nur nach Rückfrage überschreiben
    if pfad.exists():
        if not frage_ja_nein("Datei existiert bereits. "
                             "Überschreiben? (j/n)"):
            print("Rapport nicht gespeichert.")
            return
    zeilen = baue_rapport(monat, monats_eintraege, einstellungen)
    if schreibe_zeilen_in_datei(pfad, zeilen):
        print(f"Rapport gespeichert als {baue_rapport_dateiname(monat)}")
