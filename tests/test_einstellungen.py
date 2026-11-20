# Automatische Tests für US-01 bis US-03 (Speichern und Laden der Werte).
# Die Tests arbeiten mit einer eigenen Testdatei und fassen die echte
# Datei daten/einstellungen.txt nicht an.
# Start im Hauptordner: python -m tests.test_einstellungen
from pathlib import Path

from src.einstellungen import lade_einstellungen, speichere_einstellungen

TESTDATEN = Path(__file__).resolve().parent / "testdaten"
DATEI = TESTDATEN / "einstellungen_test.txt"

# Falls ein früherer Lauf abgebrochen ist: Testdatei zuerst löschen
if DATEI.exists():
    DATEI.unlink()

# Test 1: speichern und wieder laden gibt dieselben Werte
test = {
    "stundenlohn": 32.5,
    "soll_min": 480,
    "zuschlag": 25.0,
    "ahv": 5.3,
    "alv": 1.1,
    "nbu": 3.74,
}
speichere_einstellungen(test, DATEI)
assert lade_einstellungen(DATEI) == test

# Test 2: der Stundenlohn steht mit zwei Nachkommastellen in der Datei
with open(DATEI, "r", encoding="utf-8") as datei:
    erste_zeile = datei.readline().strip()
assert erste_zeile == "stundenlohn=32.50"

# Test 3: kaputte Zeile wird übersprungen, Standardwert gilt
with open(DATEI, "w", encoding="utf-8") as datei:
    datei.write("stundenlohn=abc\n")
assert lade_einstellungen(DATEI)["stundenlohn"] == 30.0

# Test 4: fehlende Werte werden mit den Standardwerten aufgefüllt
assert lade_einstellungen(DATEI)["soll_min"] == 480

# Test 5: leere Zeilen führen nicht zum Absturz
with open(DATEI, "w", encoding="utf-8") as datei:
    datei.write("stundenlohn=34.00\n\n\n")
assert lade_einstellungen(DATEI)["stundenlohn"] == 34.0

# Test 6: Datei fehlt, dann gelten die Standardwerte und die Datei
# wird angelegt
DATEI.unlink()
assert lade_einstellungen(DATEI)["stundenlohn"] == 30.0
assert DATEI.exists()

# Test 7: US-03, Prozentwerte stehen ohne unnötige .0 in der Datei
speichere_einstellungen(test, DATEI)
inhalt = DATEI.read_text(encoding="utf-8")
assert "zuschlag=25\n" in inhalt
assert "ahv=5.3\n" in inhalt
assert "alv=1.1\n" in inhalt
assert "nbu=3.74\n" in inhalt

# Testdatei wieder löschen
DATEI.unlink()


# Test 8: kaputte Zeichen in der Datei: es gelten die Standardwerte
DATEI.write_bytes(b"stundenlohn=\xff\xfe\nsoll_min=450\n")
einstellungen = lade_einstellungen(DATEI)
assert einstellungen["stundenlohn"] == 30.0
assert einstellungen["soll_min"] == 450

# Test 9: speichern gibt True zurück
assert speichere_einstellungen(test, DATEI) is True
DATEI.unlink()

print("Alle Tests bestanden")
