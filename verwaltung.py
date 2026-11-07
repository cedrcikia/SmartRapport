def eintraege_des_monats(eintraege, monat): 
    # Gibt alle Einträge eines Monats zurück, nach Datum sortiert
    # eintraege: Liste aller Einträge (Dictionaries)
    # Wird für US-07, US-08 und von Rafa (Berechnung,Rapport) gebraucht.

    # Teil A, Schritt 1: Nur die Einträge des gewählten Monats behalten
    
    gefunden = []
    for eintrag in eintraege:
        datum = eintrag["datum"]
        # Ab Position 3 steht der Monat "05.10.2026" -> "10.2026"
        if datum[3:] == monat:
            gefunden.append(eintrag)
    
    # Teil B, Schritt 1: Alle Daten der gefundenen Einträge sammeln,
    # weil man Dictionaries nicht direkt sortieren kann
    
    daten = []
    for eintrag in gefunden:
        daten.append(eintrag["datum"])

    # Schritt 2: Die Daten sortieren. Das klappt als Text, weil alle
    # im selben Monat sind und sich nur der Tag (immer 2 Stellen) unterscheidet   
    
    daten = sorted(daten)

    # Schritt 3: Für jedes Datum (in sortierter Reihenfolge) den passenden
    # Eintrag suchen und anhängen. Pro Datum gibt es nur einen Eintrag.
    
    sortiert = []
    for datum in daten:
        for eintrag in gefunden:
            if eintrag["datum"] == datum:
                sortiert.append(eintrag)
    return sortiert 


# DUMMY – wird später durch frage_monat() aus hilfen.py ersetzt
def frage_monat():
    return input("Monat (MM.JJJJ): ")


# DUMMY – wird später durch zeit_zu_minuten() aus hilfen.py ersetzt
def zeit_zu_minuten(text):
    # "07:30" -> 7 * 60 + 30 = 450
    stunden = int(text[0:2])
    minuten = int(text[3:5])
    return stunden * 60 + minuten


# DUMMY – wird später durch arbeitszeit_minuten() aus hilfen.py ersetzt
def arbeitszeit_minuten(eintrag):
    # Ende minus Start minus Pause (README, Festlegung 2)
    start = zeit_zu_minuten(eintrag["start"])
    ende = zeit_zu_minuten(eintrag["ende"])
    return ende - start - eintrag["pause_min"]


# DUMMY – wird später durch minuten_zu_text() aus hilfen.py ersetzt
def minuten_zu_text(minuten):
    # 525 -> "8 Std 45 Min"
    stunden = minuten // 60
    rest = minuten % 60
    return f"{stunden} Std {rest:02d} Min"


# DUMMY – wird später durch frage_ja_nein() aus hilfen.py ersetzt
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


# DUMMY – wird später durch speichere_eintraege() aus speicher.py ersetzt (US-06)
def speichere_eintraege(eintraege):
    # Schreibt noch nichts in stunden.txt, zeigt nur, dass gespeichert würde
    print(f"(DUMMY) stunden.txt gespeichert: {len(eintraege)} Einträge")


# DUMMY – wird später durch datum_existiert() aus hilfen.py ersetzt
def datum_existiert(eintraege, datum):
    # True, wenn es für dieses Datum schon einen Eintrag gibt
    for eintrag in eintraege:
        if eintrag["datum"] == datum:
            return True
    return False


# DUMMY – wird später durch frage_datum() aus erfassen.py ersetzt
def frage_datum(eintraege):
    # Fragt ein Datum ab, bis es dafür noch keinen Eintrag gibt
    # (das Format prüft erst die richtige Version von Leonard)
    datum = input("Datum (TT.MM.JJJJ): ")
    while datum_existiert(eintraege, datum):
        print("Für dieses Datum gibt es schon einen Eintrag.")
        datum = input("Datum (TT.MM.JJJJ): ")
    return datum


# DUMMY – wird später durch frage_uhrzeit() aus erfassen.py ersetzt
def frage_uhrzeit(text):
    # Fragt eine Uhrzeit ab (ohne Prüfung, die macht Leonards Version)
    return input(text)


# DUMMY – wird später durch frage_pause() aus erfassen.py ersetzt
def frage_pause(max_min):
    # Fragt die Pause ab, bis sie kürzer als max_min ist
    # (Eingaben wie "abc" prüft erst die richtige Version von Leonard)
    pause = int(input("Pause in Minuten: "))
    while pause >= max_min:
        print("Die Pause muss kürzer sein als die Zeit zwischen Start und Ende.")
        pause = int(input("Pause in Minuten: "))
    return pause


def zeige_liste(gefunden):
    # Zeigt die Einträge nummeriert ab 1 an und darunter das Total.
    # gefunden: Liste der Einträge eines Monats (nicht leer).
    # Wird von zeige_eintraege (US-07) und aendern_loeschen (US-08) gebraucht.
    nummer = 0
    total = 0
    for eintrag in gefunden:
        nummer += 1
        datum = eintrag["datum"]
        start = eintrag["start"]
        ende = eintrag["ende"]
        pause = eintrag["pause_min"]
        minuten = arbeitszeit_minuten(eintrag)
        print(f"{nummer}. {datum}  {start}–{ende}  Pause {pause} Min  {minuten_zu_text(minuten)}")
        total += minuten
    print(f"Total: {minuten_zu_text(total)}")


def zeige_eintraege(eintraege):
    monat = frage_monat()
    gefunden = eintraege_des_monats(eintraege, monat)
    if len(gefunden) == 0:
        print(f"Keine Einträge für {monat}.")
    else:
        # Die nummerierte Liste übernimmt jetzt zeige_liste 
        zeige_liste(gefunden)


def aendern_loeschen(eintraege):
    # US-08: Eintrag eines Monats über seine Nummer wählen,
    # danach ändern (1) oder löschen (2)
    monat = frage_monat()
    gefunden = eintraege_des_monats(eintraege, monat)
    if len(gefunden) == 0: 
        print(f"Keine Einträge für {monat}.")
    else:
        zeige_liste(gefunden)
        
        # Schritt 1: Gültige Nummern als Text sammeln ("1","2",...),
        # damit eine Eingabe wie "abc" nicht zum Absturz führt
        gueltig = []
        for i in range(1, len(gefunden) + 1):
            gueltig.append(str(i))

        # Schritt 2: Nummer abfragen, bis sie gültig ist
        eingabe = input("Nummer: ")
        while eingabe not in gueltig:
            print("Ungültige Nummer.")
            eingabe = input("Nummer: ")

        # Schritt 3: Gewählten Eintrag holen (Nummer 1 = Index 0)
        nummer = int(eingabe)
        eintrag = gefunden[nummer - 1]

        # Schritt 4: Ändern oder Löschen abfragen, bis die Wahl gültig ist
        wahl = input("1 = ändern, 2 = löschen: ")
        while wahl != "1" and wahl != "2":
            print("Ungültige Wahl.")
            wahl = input("1 = ändern, 2 = löschen: ")

        # Schritt 5: Je nach Wahl ändern (1) oder löschen (2)
        if wahl == "1":
            # Schritt 7: Eintrag vorübergehend herausnehmen, damit sein
            # eigenes Datum bei der Doppelt-Prüfung erlaubt ist
            eintraege.remove(eintrag)
            # Schritt 8: Neue Werte abfragen (gleich geprüft wie US-04/US-05)
            datum = frage_datum(eintraege)
            start = frage_uhrzeit("Start (HH:MM): ")
            ende = frage_uhrzeit("Ende (HH:MM): ")
            while zeit_zu_minuten(ende) <= zeit_zu_minuten(start):
                print("Das Ende muss nach dem Start liegen.")
                ende = frage_uhrzeit("Ende (HH:MM): ")
            max_min = zeit_zu_minuten(ende) - zeit_zu_minuten(start)
            pause = frage_pause(max_min)

            # Schritt 9: Neue Werte ins Dictionary schreiben
            eintrag["datum"] = datum
            eintrag["start"] = start
            eintrag["ende"] = ende
            eintrag["pause_min"] = pause

            # Schritt 10: Eintrag wieder in die Liste legen und speichern
            eintraege.append(eintrag)
            speichere_eintraege(eintraege)
        else: 
            # Schritt 6: Nachfragen, dann aus der ganzen Liste löschen und speichern
            if frage_ja_nein("Wirklich löschen? (j/n)"):
                eintraege.remove(eintrag)
                speichere_eintraege(eintraege)
