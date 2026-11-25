# Führt alle Tests nacheinander aus.
# Start im Hauptordner: python -m tests.alle_tests
import tests.test_berechnung
import tests.test_einstellungen
import tests.test_erinnerung
import tests.test_hilfen
import tests.test_menue
import tests.test_rapport
import tests.test_speicher

print("Alle Test-Dateien erfolgreich durchlaufen")
