# main.py · Person B · Hauptmenü von SmartRapport (Festlegung 8)

from einstellungen import lade_einstellungen, stundenlohn_eingeben


def main():
    """Zeigt das Hauptmenü, bis der Benutzer 9 wählt."""
    # Einstellungen einmal beim Start laden (Festlegung 7)
    einstellungen = lade_einstellungen()

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

        if wahl == "6":
            stundenlohn_eingeben(einstellungen)
        elif wahl == "9":
            print("Auf Wiedersehen!")
            break  # einziger Ausgang aus der Schleife
        elif wahl in ["1", "2", "3", "4", "5", "7", "8"]:
            # Platzhalter, bis die anderen Funktionen fertig sind
            print("Noch nicht umgesetzt.")
        else:
            print("Ungültige Wahl.")


# Startet das Menü nur, wenn main.py direkt ausgeführt wird
if __name__ == "__main__":
    main()
