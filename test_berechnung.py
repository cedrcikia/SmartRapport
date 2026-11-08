# Automatische Tests für US-10 und die Lohnrechnung (US-11).
# Die Werte stammen aus den Akzeptanzkriterien im README.
from berechnung import berechne_ueberstunden, berechne_monat

# Sollzeit 8 Std 00 Min = 480 Min
SOLL = 480


def tag(start, ende, pause_min):
    """Kleiner Helfer: baut einen Eintrag, das Datum ist hier egal."""
    return {"datum": "05.10.2026", "start": start, "ende": ende,
            "pause_min": pause_min}


# Test 1: 10:00 Arbeitszeit, also 8:00 normal und 2:00 Überstunden
assert berechne_ueberstunden([tag("08:00", "18:00", 0)], SOLL) == (480, 120)

# Test 2: genau die Sollzeit, keine Überstunden
assert berechne_ueberstunden([tag("08:00", "16:00", 0)], SOLL) == (480, 0)

# Test 3: weniger als die Sollzeit (7:30), alles normal
assert berechne_ueberstunden([tag("08:00", "15:30", 0)], SOLL) == (450, 0)

# Test 4: zwei Tage (8 Std 45 Min und 7 Std 30 Min)
zwei_tage = [tag("07:30", "17:00", 45), tag("08:00", "16:00", 30)]
assert berechne_ueberstunden(zwei_tage, SOLL) == (930, 45)

# Test 5: Monat ohne Einträge
assert berechne_ueberstunden([], SOLL) == (0, 0)

# Test 6: Lohnübersicht aus US-11 (Lohn 32.50, Zuschlag 25 %,
# AHV 5.3 %, ALV 1.1 %, NBU 0.8 %)
einstellungen = {"soll_min": 480, "stundenlohn": 32.50, "zuschlag": 25,
                 "ahv": 5.3, "alv": 1.1, "nbu": 0.8}
ergebnis = berechne_monat(zwei_tage, einstellungen)
assert ergebnis["normal_min"] == 930
assert ergebnis["ueber_min"] == 45
assert ergebnis["brutto"] == 534.22
assert ergebnis["abzuege"] == {"AHV": 28.31, "ALV": 5.88, "NBU": 4.27}
assert ergebnis["netto"] == 495.76

# Test 7: alle Abzüge 0 %, dann ist Netto gleich Brutto
einstellungen_ohne = dict(einstellungen, ahv=0, alv=0, nbu=0)
ergebnis = berechne_monat(zwei_tage, einstellungen_ohne)
assert ergebnis["netto"] == ergebnis["brutto"]

# Test 8: Monat ohne Einträge gibt überall 0
ergebnis = berechne_monat([], einstellungen)
assert ergebnis["brutto"] == 0 and ergebnis["netto"] == 0

print("Alle Tests bestanden")
