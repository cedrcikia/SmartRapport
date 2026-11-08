# hilfen.py · Person A · Hilfsfunktionen für das ganze Team


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


def frage_monat():
    return input("Monat (MM.JJJJ): ")


def zeit_zu_minuten(text):
    # "07:30" -> 7 * 60 + 30 = 450
    stunden = int(text[0:2])
    minuten = int(text[3:5])
    return stunden * 60 + minuten


def arbeitszeit_minuten(eintrag):
    # Ende minus Start minus Pause (README, Festlegung 2)
    start = zeit_zu_minuten(eintrag["start"])
    ende = zeit_zu_minuten(eintrag["ende"])
    return ende - start - eintrag["pause_min"]


def minuten_zu_text(minuten):
    # 525 -> "8 Std 45 Min"
    stunden = minuten // 60
    rest = minuten % 60
    return f"{stunden} Std {rest:02d} Min"


def frage_ja_nein(frage):
    # Fragt so lange, bis "j" oder "n" eingegeben wird.
    # Gibt True zurück bei "j", False bei "n".
    antwort = input(frage + " ")
    while antwort != "j" and antwort != "n":
        print("Bitte j oder n eingeben.")
        antwort = input(frage + " ")
    if antwort == "j":
        return True
    else:
        return False


def datum_existiert(eintraege, datum):
    # True, wenn es für dieses Datum schon einen Eintrag gibt
    for eintrag in eintraege:
        if eintrag["datum"] == datum:
            return True
    return False
