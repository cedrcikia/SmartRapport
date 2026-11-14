# Automatische Tests für US-04 (Prüfungen) und US-09 (Erinnerung).
# Die Werte stammen aus den Akzeptanzkriterien im README.
from datetime import date
from pathlib import Path

from erfassen import ist_gueltiges_datum, ist_gueltige_uhrzeit
from erinnerung import erinnerung_text

# US-04: Datum
assert ist_gueltiges_datum("05.10.2026") == True
assert ist_gueltiges_datum("31.02.2026") == False
assert ist_gueltiges_datum("5.10.26") == False
assert ist_gueltiges_datum("abc") == False
assert ist_gueltiges_datum("29.02.2028") == True   # Schaltjahr

# US-04: Uhrzeit
assert ist_gueltige_uhrzeit("07:30") == True
assert ist_gueltige_uhrzeit("23:59") == True
assert ist_gueltige_uhrzeit("7:30") == False
assert ist_gueltige_uhrzeit("24:00") == False
assert ist_gueltige_uhrzeit("25:00") == False
assert ist_gueltige_uhrzeit("abc") == False

# US-09: nur testen, wenn die Rapport-Dateien nicht schon existieren
if not Path("rapport_10_2026.txt").exists():
    assert erinnerung_text(date(2026, 10, 28)) == \
        "Rapport Oktober bis 31.10.2026 abgeben – noch 3 Tage"
    assert erinnerung_text(date(2026, 10, 30)).endswith("noch 1 Tag")
    assert erinnerung_text(date(2026, 10, 31)).endswith("noch 0 Tage")
    assert erinnerung_text(date(2026, 10, 27)) == ""

    # Rapport existiert: keine Erinnerung (Datei danach wieder löschen)
    Path("rapport_10_2026.txt").write_text("test", encoding="utf-8")
    assert erinnerung_text(date(2026, 10, 28)) == ""
    Path("rapport_10_2026.txt").unlink()

if not Path("rapport_02_2026.txt").exists():
    assert erinnerung_text(date(2026, 2, 25)) == \
        "Rapport Februar bis 28.02.2026 abgeben – noch 3 Tage"

# 01.11.2026: keine Erinnerung für Oktober (November ist noch weit weg)
assert erinnerung_text(date(2026, 11, 1)) == ""

print("Alle Tests bestanden")
