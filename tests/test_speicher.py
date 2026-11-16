# Automatische Tests für US-06 (Einträge speichern und laden).
# Start im Hauptordner: python -m tests.test_speicher
from pathlib import Path

from src.speicher import (ist_gueltige_zeile, lade_eintraege,
                          speichere_eintraege, wandle_eintrag_in_zeile_um)

TESTDATEN = Path(__file__).resolve().parent / "testdaten"
TESTDATEI = TESTDATEN / "stunden_test.txt"

eintrag = {"datum": "05.10.2026", "start": "07:30", "ende": "17:00",
           "pause_min": 45}

# Test 1: ein Eintrag wird zu einer Zeile
assert wandle_eintrag_in_zeile_um(eintrag) == "05.10.2026;07:30;17:00;45"

# Test 2: gültige und ungültige Zeilen
assert ist_gueltige_zeile(["05.10.2026", "07:30", "17:00", "45"])
assert not ist_gueltige_zeile(["05.10.2026", "07:30", "abc", "45"])
assert not ist_gueltige_zeile(["05.10.2026", "07:30"])
assert not ist_gueltige_zeile(["31.02.2026", "07:30", "17:00", "45"])
assert not ist_gueltige_zeile(["05.10.2026", "17:00", "07:30", "45"])
assert not ist_gueltige_zeile(["05.10.2026", "07:30", "17:00", "570"])
assert not ist_gueltige_zeile(["05.10.2026", "07:30", "17:00", "4.5"])

# Test 3: drei gültige Zeilen werden alle geladen
assert len(lade_eintraege(TESTDATEN / "stunden_beispiel.txt")) == 3

# Test 4: kaputte Zeile und doppeltes Datum werden übersprungen
geladen = lade_eintraege(TESTDATEN / "stunden_fehler.txt")
assert len(geladen) == 1
assert geladen[0]["datum"] == "05.10.2026"

# Test 5: fehlende Datei gibt eine leere Liste
assert lade_eintraege(TESTDATEN / "gibt_es_nicht.txt") == []

# Test 6: speichern und wieder laden gibt dieselben Einträge
speichere_eintraege([eintrag], TESTDATEI)
assert lade_eintraege(TESTDATEI) == [eintrag]
TESTDATEI.unlink()

print("Alle Tests bestanden")
