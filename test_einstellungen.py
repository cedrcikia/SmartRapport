# Automatische Tests für US-01.
# Die Tests ändern einstellungen.txt. Darum wird der Inhalt vorher
# gesichert und am Schluss wieder zurückgeschrieben.
from pathlib import Path

from einstellungen import speichere_einstellungen, lade_einstellungen

DATEI = Path("einstellungen.txt")

# Echte Einstellungen sichern, damit sie nach dem Test nicht weg sind
gesichert = None
if DATEI.exists():
    gesichert = DATEI.read_text(encoding="utf-8")

# Test 1: speichern und wieder laden gibt dieselben Werte
test = {
    "stundenlohn": 32.5,
    "soll_min": 480,
    "zuschlag": 25.0,
    "ahv": 5.3,
    "alv": 1.1,
    "nbu": 3.74,
}
speichere_einstellungen(test)
assert lade_einstellungen() == test

# Test 2: der Stundenlohn steht mit zwei Nachkommastellen in der Datei
with open(DATEI, "r", encoding="utf-8") as datei:
    erste_zeile = datei.readline().strip()
assert erste_zeile == "stundenlohn=32.50"

# Test 3: kaputte Zeile wird übersprungen, Standardwert gilt
with open(DATEI, "w", encoding="utf-8") as datei:
    datei.write("stundenlohn=abc\n")
assert lade_einstellungen()["stundenlohn"] == 30.0

# Test 4: fehlende Werte werden mit den Standardwerten aufgefüllt
assert lade_einstellungen()["soll_min"] == 480

# Test 5: leere Zeilen führen nicht zum Absturz
with open(DATEI, "w", encoding="utf-8") as datei:
    datei.write("stundenlohn=34.00\n\n\n")
assert lade_einstellungen()["stundenlohn"] == 34.0

# Test 6: Datei fehlt, dann gelten die Standardwerte
DATEI.unlink()
assert lade_einstellungen()["stundenlohn"] == 30.0

# Test 7: US-03, Prozentwerte stehen ohne unnötige .0 in der Datei
speichere_einstellungen(test)
inhalt = DATEI.read_text(encoding="utf-8")
assert "zuschlag=25\n" in inhalt
assert "ahv=5.3\n" in inhalt
assert "alv=1.1\n" in inhalt
assert "nbu=3.74\n" in inhalt
# Echte Einstellungen zurückschreiben
if gesichert is not None:
    DATEI.write_text(gesichert, encoding="utf-8")

print("Alle Tests bestanden")
