# Automatische Tests für US-01. Achtung: überschreibt einstellungen.txt.
from einstellungen import speichere_einstellungen, lade_einstellungen

# Test 1: speichern und wieder laden gibt dieselben Werte
test = {"stundenlohn": 32.5, "soll_min": 480, "zuschlag": 25.0, "ahv": 5.3, "alv": 1.1, "nbu": 3.74}
speichere_einstellungen(test)
assert lade_einstellungen() == test

# Test 2: der Stundenlohn steht mit zwei Nachkommastellen in der Datei
with open("einstellungen.txt", "r") as datei:
    erste_zeile = datei.readline().strip()
assert erste_zeile == "stundenlohn=32.50"

# Test 3: kaputte Zeile wird übersprungen, Standardwert gilt
with open("einstellungen.txt", "w") as datei:
    datei.write("stundenlohn=abc\n")
assert lade_einstellungen()["stundenlohn"] == 30.0

# Test 4: fehlende Werte werden mit den Standardwerten aufgefüllt
assert lade_einstellungen()["soll_min"] == 480

# Test 5: leere Zeilen führen nicht zum Absturz
with open("einstellungen.txt", "w") as datei:
    datei.write("stundenlohn=34.00\n\n\n")
assert lade_einstellungen()["stundenlohn"] == 34.0

# Test 6: Datei fehlt, dann gelten die Standardwerte
from pathlib import Path
Path("einstellungen.txt").unlink()
assert lade_einstellungen()["stundenlohn"] == 30.0

print("Alle Tests bestanden")