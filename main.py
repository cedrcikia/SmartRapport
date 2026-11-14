# main.py · Person B · Hauptmenü von SmartRapport (Festlegung 8)

from datetime import date

from berechnung import zeige_uebersicht
from einstellungen import (lade_einstellungen, sollzeit_eingeben,
                           stundenlohn_eingeben)
from erfassen import arbeitstag_eintragen
from erinnerung import pruefe_erinnerung
from rapport import rapport_speichern
from verwaltung import aendern_loeschen, zeige_eintraege


# DUMMY – wird später durch lade_eintraege() aus speicher.py ersetzt (US-06)
def lade_eintraege():
    # Liest noch nicht aus stunden.txt, startet mit leerer Liste
    return []


# DUMMY – wird später durch saetze_eingeben() aus einstellungen.py ersetzt (US-03)
def saetze_eingeben(einstellungen):
    print("Noch nicht umgesetzt.")


def main():
    """Startablauf laut Teamplan, dann Hauptmenü, bis der Benutzer 9 wählt."""
    # Einstellungen und Einträge einmal beim Start laden (Festlegung 7)
    einstellungen = lade_einstellungen()
    eintraege = lade_eintraege()

    # US-09: beim Start an den Abgabetermin erinnern
    pruefe_erinnerung(date.today())

    # Endlosschleife, damit das Menü nach jeder Funktion wieder erscheint
    while True:
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

        # Vergleich als Text statt int(): so stürzt "abc" nicht ab
        wahl = input("Deine Wahl: ")

        if wahl == "1":
            arbeitstag_eintragen(eintraege)
        elif wahl == "2":
            zeige_eintraege(eintraege)
        elif wahl == "3":
            aendern_loeschen(eintraege)
        elif wahl == "4":
            zeige_uebersicht(eintraege, einstellungen)
        elif wahl == "5":
            rapport_speichern(eintraege, einstellungen)
        elif wahl == "6":
            stundenlohn_eingeben(einstellungen)
        elif wahl == "7":
            sollzeit_eingeben(einstellungen)
        elif wahl == "8":
            saetze_eingeben(einstellungen)
        elif wahl == "9":
            # alles wurde schon beim Ändern gespeichert, darum nur Abschied
            print("Auf Wiedersehen!")
            break  # einziger Ausgang aus der Schleife
        else:
            # 0, 10, abc oder leer
            print("Ungültige Wahl.")


# Startet das Menü nur, wenn main.py direkt ausgeführt wird
if __name__ == "__main__":
    main()
