# Automatische Tests für US-12. Geprüft werden die Funktionen, die den
# Text bauen. Das Beispiel stammt aus den Akzeptanzkriterien im README.
from hilfen import rapport_dateiname, abgabetermin
from rapport import baue_rapport

eintraege = [
    {"datum": "05.10.2026", "start": "07:30", "ende": "17:00",
     "pause_min": 45},
    {"datum": "06.10.2026", "start": "08:00", "ende": "16:00",
     "pause_min": 30},
]
einstellungen = {"soll_min": 480, "stundenlohn": 32.50, "zuschlag": 25,
                 "ahv": 5.3, "alv": 1.1, "nbu": 3.74}

# Test 1: Dateiname aus dem Monat
assert rapport_dateiname("10.2026") == "rapport_10_2026.txt"

# Test 2: Abgabetermin ist der letzte Tag des Monats
assert abgabetermin("10.2026") == "31.10.2026"
assert abgabetermin("11.2026") == "30.11.2026"
assert abgabetermin("02.2026") == "28.02.2026"
assert abgabetermin("02.2028") == "29.02.2028"

# Test 3: der ganze Rapport stimmt mit dem Beispiel im README überein
erwartet = [
    "SMARTRAPPORT - RAPPORT 10.2026",
    "Abgabetermin: 31.10.2026",
    "-" * 40,
    "1. 05.10.2026  07:30-17:00  Pause 45 Min  8 Std 45 Min",
    "2. 06.10.2026  08:00-16:00  Pause 30 Min  7 Std 30 Min",
    "Total: 16 Std 15 Min",
    "-" * 40,
    "Normalstunden:     15 Std 30 Min",
    "Überstunden:        0 Std 45 Min",
    "Brutto:            CHF 534.22",
    "AHV (5.30 %):      -CHF 28.31",
    "ALV (1.10 %):      -CHF 5.88",
    "NBU (3.74 %):      -CHF 19.98",
    "Netto:             CHF 480.05",
]
assert baue_rapport("10.2026", eintraege, einstellungen) == erwartet

print("Alle Tests bestanden")
