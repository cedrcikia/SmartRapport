def eintraege_des_monats(eintraege, monat): 
    # Gibt alle Einträge eines Monats zurück, nach Datum sortiert
    # eintraege: Liste aller Einträge (Dictionaries)
    # Wird für US-07, US-08 und von Rafa (Berechnung,Rapport) gebraucht.

    # Teil A, Schritt 1: Nur die Einträge des gewählten Monats behalten
    
    gefunden = []
    for eintrag in eintraege:
        datum = eintrag["datum"]
        # Ab Position 3 steht der Monat "05.10.2026 -> "10.2026"
        if datum[3:] == monat:
            gefunden.append(eintrag)
    
    # Teil B, Schritt 1: Alle Daten der gefundenen Einträge sammeln,
    # weil man Dictionaries nicht direkt sortieren kann
    
    daten = []
    for eintrag in gefunden:
        daten.append(eintrag["datum"])

    # Schritt 2: Die Daten Sortieren. Das klappt als Text weil alle
    # im selben monat sind und sich nur der Tag (immer 2 Stellen) unterscheidet   
    
    daten = sorted(daten)

    # Schritt 3: Für jedes Datum (in sortierter Reihenfolge) den passenden
    # Eintrag suchen und anhängen. Pro Datum gibt es nur einen Eintrag.
    
    sortiert = []
    for datum in daten:
        for eintrag in gefunden:
            if eintrag["datum"] == datum:
                sortiert.append(eintrag)
    return sortiert 
