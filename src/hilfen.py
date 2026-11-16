# hilfen.py · Person A · Hilfsfunktionen für das ganze Team
# Prüfen, Umwandeln und Fragen, die mehrere Dateien brauchen.

from src.pfade import DATEN_ORDNER


# ---------- Eingaben prüfen ----------

def ist_nur_ziffern(text):
    """True, wenn der Text nicht leer ist und nur Ziffern hat."""
    if len(text) == 0:
        return False
    for zeichen in text:
        if zeichen not in "0123456789":
            return False
    return True


def ist_dezimalzahl(text):
    """True bei einer Zahl wie 32.50 oder 5 (Ziffern und höchstens ein Punkt).
    Ein Komma (32,50) ist ungültig.
    """
    return text.replace(".", "", 1).isdecimal()


def ist_gueltiges_datum(text):
    """Prüft TT.MM.JJJJ und ob es das Datum wirklich gibt."""
    if len(text) != 10 or text[2] != "." or text[5] != ".":
        return False
    if not ist_nur_ziffern(text[0:2] + text[3:5] + text[6:10]):
        return False
    tag = int(text[0:2])
    monat_nummer = int(text[3:5])
    jahr = int(text[6:10])
    if monat_nummer < 1 or monat_nummer > 12:
        return False
    if tag < 1 or tag > zaehle_tage_im_monat(monat_nummer, jahr):
        return False
    return True


def ist_gueltige_uhrzeit(text):
    """Prüft HH:MM von 00:00 bis 23:59 (7:30 und 24:00 sind ungültig)."""
    if len(text) != 5 or text[2] != ":":
        return False
    if not ist_nur_ziffern(text[0:2] + text[3:5]):
        return False
    stunden = int(text[0:2])
    minuten = int(text[3:5])
    return stunden <= 23 and minuten <= 59


def ist_gueltiger_monat(text):
    """Prüft MM.JJJJ, Monat 01 bis 12."""
    if len(text) != 7 or text[2] != ".":
        return False
    if not ist_nur_ziffern(text[0:2] + text[3:7]):
        return False
    monat_nummer = int(text[0:2])
    return 1 <= monat_nummer <= 12


# ---------- Datum, Zeit und Dauer umwandeln ----------

def zaehle_tage_im_monat(monat_nummer, jahr):
    """Wie viele Tage hat der Monat? Februar: 29 im Schaltjahr, sonst 28."""
    if monat_nummer == 2:
        if jahr % 4 == 0 and (jahr % 100 != 0 or jahr % 400 == 0):
            return 29
        return 28
    if monat_nummer in (4, 6, 9, 11):
        return 30
    return 31


def wandle_zeit_in_minuten_um(text):
    """Wandelt "07:30" in Minuten um: 7 * 60 + 30 = 450."""
    stunden = int(text[0:2])
    minuten = int(text[3:5])
    return stunden * 60 + minuten


def wandle_minuten_in_text_um(gesamt_min):
    """Wandelt Minuten in Text um: 525 wird zu "8 Std 45 Min"."""
    stunden = gesamt_min // 60
    rest = gesamt_min % 60
    return f"{stunden} Std {rest:02d} Min"


def berechne_arbeitszeit_min(eintrag):
    """Arbeitszeit in Minuten: Ende minus Start minus Pause (Festlegung 2)."""
    start = wandle_zeit_in_minuten_um(eintrag["start"])
    ende = wandle_zeit_in_minuten_um(eintrag["ende"])
    return ende - start - eintrag["pause_min"]


# ---------- Einträge ----------

def filtere_eintraege_nach_monat(eintraege, monat):
    """Gibt alle Einträge eines Monats zurück, nach Datum sortiert.
    eintraege: Liste aller Einträge (Dictionaries), monat: z.B. "10.2026".
    Wird von US-07, US-08, US-11 und US-12 gebraucht.
    """
    # Schritt 1: nur die Einträge des gewählten Monats behalten
    monats_eintraege = []
    for eintrag in eintraege:
        # Ab Position 3 steht der Monat: "05.10.2026" -> "10.2026"
        if eintrag["datum"][3:] == monat:
            monats_eintraege.append(eintrag)

    # Schritt 2: alle Daten sammeln und sortieren. Das klappt als Text,
    # weil alle im selben Monat liegen und der Tag immer 2 Stellen hat
    datumsliste = []
    for eintrag in monats_eintraege:
        datumsliste.append(eintrag["datum"])
    datumsliste = sorted(datumsliste)

    # Schritt 3: für jedes Datum den passenden Eintrag anhängen
    # (pro Datum gibt es nur einen Eintrag)
    sortiert = []
    for datum in datumsliste:
        for eintrag in monats_eintraege:
            if eintrag["datum"] == datum:
                sortiert.append(eintrag)
    return sortiert


def hat_eintrag_fuer_datum(eintraege, datum):
    """True, wenn es für dieses Datum schon einen Eintrag gibt."""
    for eintrag in eintraege:
        if eintrag["datum"] == datum:
            return True
    return False


# ---------- Rapport: Termin und Dateiname ----------

def berechne_abgabetermin(monat):
    """Letzter Tag des Monats als Text: "10.2026" wird zu "31.10.2026"."""
    monat_nummer = int(monat[0:2])
    jahr = int(monat[3:7])
    letzter_tag = zaehle_tage_im_monat(monat_nummer, jahr)
    return f"{letzter_tag:02d}.{monat}"


def baue_rapport_dateiname(monat):
    """Dateiname des Rapports: "10.2026" wird zu "rapport_10_2026.txt"."""
    return "rapport_" + monat[0:2] + "_" + monat[3:7] + ".txt"


def baue_rapport_pfad(monat, ordner=DATEN_ORDNER):
    """Voller Pfad des Rapports im Ordner daten/ (oder in einem anderen)."""
    return ordner / baue_rapport_dateiname(monat)


# ---------- Fragen ----------

def frage_ja_nein(frage):
    """Fragt, bis "j" oder "n" eingegeben wird. Gibt True bei "j" zurück."""
    eingabe = input(frage + " ")
    while eingabe != "j" and eingabe != "n":
        print("Bitte j oder n eingeben.")
        eingabe = input(frage + " ")
    return eingabe == "j"


def frage_monat():
    """Fragt den Monat, bis er gültig ist, und gibt ihn zurück."""
    eingabe = input("Monat (MM.JJJJ): ")
    while not ist_gueltiger_monat(eingabe):
        print("Ungültiger Monat (MM.JJJJ).")
        eingabe = input("Monat (MM.JJJJ): ")
    return eingabe
