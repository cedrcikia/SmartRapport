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


def rapport_dateiname(monat):
    # "10.2026" -> "rapport_10_2026.txt"
    return "rapport_" + monat[0:2] + "_" + monat[3:7] + ".txt"


def abgabetermin(monat):
    # Letzter Tag des Monats als Text: "10.2026" -> "31.10.2026"
    mm = int(monat[0:2])
    jahr = int(monat[3:7])
    letzter_tag = tage_im_monat(mm, jahr)
    return f"{letzter_tag:02d}.{monat}"


def tage_im_monat(monat, jahr):
    # Wie viele Tage hat der Monat? Februar: 29 im Schaltjahr, sonst 28
    if monat == 2:
        if jahr % 4 == 0 and (jahr % 100 != 0 or jahr % 400 == 0):
            return 29
        return 28
    if monat == 4 or monat == 6 or monat == 9 or monat == 11:
        return 30
    return 31


def ist_gueltiges_datum(text):
    # Prüft TT.MM.JJJJ und ob es das Datum wirklich gibt
    if len(text) != 10 or text[2] != "." or text[5] != ".":
        return False
    if not (text[0:2] + text[3:5] + text[6:10]).isdecimal():
        return False
    tag = int(text[0:2])
    monat = int(text[3:5])
    jahr = int(text[6:10])
    if monat < 1 or monat > 12:
        return False
    if tag < 1 or tag > tage_im_monat(monat, jahr):
        return False
    return True


def ist_gueltige_uhrzeit(text):
    # Prüft HH:MM von 00:00 bis 23:59
    if len(text) != 5 or text[2] != ":":
        return False
    if not (text[0:2] + text[3:5]).isdecimal():
        return False
    stunden = int(text[0:2])
    minuten = int(text[3:5])
    if stunden > 23 or minuten > 59:
        return False
    return True


def ist_gueltiger_monat(text):
    # Prüft MM.JJJJ, Monat 01 bis 12
    if len(text) != 7 or text[2] != ".":
        return False
    if not (text[0:2] + text[3:7]).isdecimal():
        return False
    monat = int(text[0:2])
    if monat < 1 or monat > 12:
        return False
    return True


def frage_monat():
    # Fragt den Monat, bis er gültig ist, und gibt ihn zurück
    text = input("Monat (MM.JJJJ): ")
    while not ist_gueltiger_monat(text):
        print("Ungültiger Monat (MM.JJJJ).")
        text = input("Monat (MM.JJJJ): ")
    return text
