# main.py · Person B · Hauptmenü von SmartRapport (Festlegung 8)
# Start der App: python main.py

from datetime import date

from src.berechnung import zeige_uebersicht
from src.einstellungen import (aendere_sollzeit, aendere_stundenlohn,
                               aendere_zuschlag_und_abzuege,
                               lade_einstellungen)
from src.erfassung import trage_arbeitstag_ein
from src.erinnerung import zeige_erinnerung
from src.pfade import lege_daten_ordner_an
from src.rapport import speichere_rapport
from src.speicher import lade_eintraege
from src.verwaltung import aendere_oder_loesche_eintrag, zeige_eintraege


def zeige_hauptmenue():
    """Zeigt das Hauptmenü mit den Punkten 1 bis 9."""
    print()
    print("[SMARTRAPPORT - HAUPTMENÜ]")
    print("1. Arbeitstag eintragen")
    print("2. Einträge anzeigen")
    print("3. Eintrag ändern oder löschen")
    print("4. Übersicht anzeigen")
    print("5. Rapport speichern")
    print("6. Stundenlohn ändern")
    print("7. Sollzeit ändern")
    print("8. Zuschlag und Abzüge ändern")
    print("9. Beenden")


def starte_app():
    """Startablauf laut Teamplan, dann Hauptmenü, bis der Benutzer 9 wählt."""
    # Ordner für die Dateien anlegen, dann Einstellungen und Einträge
    # einmal beim Start laden (Festlegung 7)
    lege_daten_ordner_an()
    einstellungen = lade_einstellungen()
    eintraege = lade_eintraege()

    # US-09: beim Start an den Abgabetermin erinnern
    zeige_erinnerung(date.today())

    # Endlosschleife, damit das Menü nach jeder Funktion wieder erscheint
    while True:
        zeige_hauptmenue()

        # Vergleich als Text statt int(): so stürzt "abc" nicht ab
        wahl = input("Deine Wahl: ")

        if wahl == "1":
            trage_arbeitstag_ein(eintraege)
        elif wahl == "2":
            zeige_eintraege(eintraege)
        elif wahl == "3":
            aendere_oder_loesche_eintrag(eintraege)
        elif wahl == "4":
            zeige_uebersicht(eintraege, einstellungen)
        elif wahl == "5":
            speichere_rapport(eintraege, einstellungen)
        elif wahl == "6":
            aendere_stundenlohn(einstellungen)
        elif wahl == "7":
            aendere_sollzeit(einstellungen)
        elif wahl == "8":
            aendere_zuschlag_und_abzuege(einstellungen)
        elif wahl == "9":
            # alles wurde schon beim Ändern gespeichert, darum nur Abschied
            print("Auf Wiedersehen!")
            break  # einziger Ausgang aus der Schleife
        else:
            # 0, 10, abc oder leer
            print("Ungültige Wahl.")


# Startet das Menü nur, wenn main.py direkt ausgeführt wird
if __name__ == "__main__":
    starte_app()
