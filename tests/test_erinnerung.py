# Automatische Tests für US-09 (Erinnerung an den Abgabetermin).
# Die Werte stammen aus den Akzeptanzkriterien im README.
# Start im Hauptordner: python -m tests.test_erinnerung
from datetime import date
from pathlib import Path

from src.erinnerung import baue_erinnerung_text

# Ordner ohne Rapport-Dateien, damit die echten Rapporte nicht stören
ORDNER = Path(__file__).resolve().parent / "testdaten"

# Erinnerung in den letzten 4 Tagen des Monats
assert baue_erinnerung_text(date(2026, 10, 28), ORDNER) == \
    "Rapport Oktober bis 31.10.2026 abgeben – noch 3 Tage"
assert baue_erinnerung_text(date(2026, 10, 30), ORDNER).endswith("noch 1 Tag")
assert baue_erinnerung_text(date(2026, 10, 31), ORDNER).endswith("noch 0 Tage")

# Februar hat 28 Tage
assert baue_erinnerung_text(date(2026, 2, 25), ORDNER) == \
    "Rapport Februar bis 28.02.2026 abgeben – noch 3 Tage"

# Vorher und nachher keine Erinnerung
assert baue_erinnerung_text(date(2026, 10, 27), ORDNER) == ""
assert baue_erinnerung_text(date(2026, 11, 1), ORDNER) == ""

# Rapport existiert schon: keine Erinnerung (Testdatei danach löschen)
rapport = ORDNER / "rapport_10_2026.txt"
rapport.write_text("test", encoding="utf-8")
assert baue_erinnerung_text(date(2026, 10, 28), ORDNER) == ""
rapport.unlink()

print("Alle Tests bestanden")
