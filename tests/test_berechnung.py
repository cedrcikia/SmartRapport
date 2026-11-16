# Automatische Tests für US-10 und die Lohnrechnung (US-11).
# Die Werte stammen aus den Akzeptanzkriterien im README.
# Start im Hauptordner: python -m tests.test_berechnung
from src.berechnung import (baue_uebersicht_zeilen, berechne_monat,
                            berechne_ueberstunden)
from src.hilfen import wandle_minuten_in_text_um

# Sollzeit 8 Std 00 Min = 480 Min
SOLL = 480


def baue_eintrag(start, ende, pause_min):
    """Kleiner Helfer: baut einen Eintrag, das Datum ist hier egal."""
    return {"datum": "05.10.2026", "start": start, "ende": ende,
            "pause_min": pause_min}


# Test 1: 10:00 Arbeitszeit, also 8:00 normal und 2:00 Überstunden
zehn_stunden = baue_eintrag("08:00", "18:00", 0)
assert berechne_ueberstunden([zehn_stunden], SOLL) == (480, 120)

# Test 2: genau die Sollzeit, keine Überstunden
acht_stunden = baue_eintrag("08:00", "16:00", 0)
assert berechne_ueberstunden([acht_stunden], SOLL) == (480, 0)

# Test 3: weniger als die Sollzeit (7:30), alles normal
halb_acht = baue_eintrag("08:00", "15:30", 0)
assert berechne_ueberstunden([halb_acht], SOLL) == (450, 0)

# Test 4: zwei Tage (8 Std 45 Min und 7 Std 30 Min)
zwei_tage = [baue_eintrag("07:30", "17:00", 45),
             baue_eintrag("08:00", "16:00", 30)]
assert berechne_ueberstunden(zwei_tage, SOLL) == (930, 45)

# Test 5: Monat ohne Einträge
assert berechne_ueberstunden([], SOLL) == (0, 0)

# Test 6: Lohnübersicht aus US-11 (Lohn 32.50, Zuschlag 25 %,
# AHV 5.3 %, ALV 1.1 %, NBU 3.74 %)
einstellungen = {"soll_min": 480, "stundenlohn": 32.50, "zuschlag": 25,
                 "ahv": 5.3, "alv": 1.1, "nbu": 3.74}
ergebnis = berechne_monat(zwei_tage, einstellungen)
assert ergebnis["normal_min"] == 930
assert ergebnis["ueber_min"] == 45
assert ergebnis["brutto"] == 534.22
assert ergebnis["abzuege"] == {"ahv": 28.31, "alv": 5.88, "nbu": 19.98}
assert ergebnis["netto"] == 480.05

# Test 7: alle Abzüge 0 %, dann ist Netto gleich Brutto
einstellungen_ohne = {"soll_min": 480, "stundenlohn": 32.50, "zuschlag": 25,
                      "ahv": 0, "alv": 0, "nbu": 0}
ergebnis = berechne_monat(zwei_tage, einstellungen_ohne)
assert ergebnis["netto"] == ergebnis["brutto"]

# Test 8: Monat ohne Einträge gibt überall 0
ergebnis = berechne_monat([], einstellungen)
assert ergebnis["brutto"] == 0 and ergebnis["netto"] == 0
assert wandle_minuten_in_text_um(ergebnis["normal_min"]) == "0 Std 00 Min"
assert wandle_minuten_in_text_um(ergebnis["ueber_min"]) == "0 Std 00 Min"

# Test 9: die Übersicht sieht genau so aus wie im README (US-11)
ergebnis = berechne_monat(zwei_tage, einstellungen)
erwartet = [
    "Normalstunden:     15 Std 30 Min",
    "Überstunden:        0 Std 45 Min",
    "Brutto:            CHF 534.22",
    "AHV (5.30 %):      -CHF 28.31",
    "ALV (1.10 %):      -CHF 5.88",
    "NBU (3.74 %):      -CHF 19.98",
    "Netto:             CHF 480.05",
]
assert baue_uebersicht_zeilen(ergebnis, einstellungen) == erwartet

print("Alle Tests bestanden")
