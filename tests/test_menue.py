# Automatische Tests für das Hauptmenü (Festlegung 8). Getestet werden
# nur die Wahlen, die nichts abfragen (9, ungültige Eingaben).
# Start im Hauptordner: python -m tests.test_menue
from main import fuehre_menuepunkt_aus

# 9 beendet das Programm: die Schleife soll aufhören (False)
assert fuehre_menuepunkt_aus("9", [], {}) is False

# 0, 10, abc und leer sind ungültig: das Menü erscheint wieder (True)
for wahl in ["0", "10", "abc", "", " "]:
    assert fuehre_menuepunkt_aus(wahl, [], {}) is True

print("Alle Tests bestanden")
