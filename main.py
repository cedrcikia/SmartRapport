# main.py · Person B · Hauptmenü von SmartRapport (Festlegung 8)

# Endlosschleife, damit das Menü nach jeder Funktion wieder erscheint
while True:
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

    # Platzhalter: werden später durch die echten Funktionen ersetzt
    if wahl == "1":
        print("Arbeitstag eintragen")
    elif wahl == "2":
        print("Einträge anzeigen")
    elif wahl == "3":
        print("Eintrag ändern oder löschen")
    elif wahl == "4":
        print("Übersicht anzeigen")
    elif wahl == "5":
        print("Rapport speichern")
    elif wahl == "6":
        print("Stundenlohn ändern")
    elif wahl == "7":
        print("Sollzeit ändern")
    elif wahl == "8":
        print("Zuschlag und Abzüge ändern")
    elif wahl == "9":
        print("Auf Wiedersehen!")
        break  # einziger Ausgang aus der Schleife
    else:
        print("Ungültige Wahl.")
