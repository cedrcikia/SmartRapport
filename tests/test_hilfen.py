# Automatische Tests für die Hilfsfunktionen (Prüfungen aus US-04 und
# US-07, Umwandlungen, Abgabetermin, Dateiname).
# Die Werte stammen aus den Akzeptanzkriterien im README.
# Start im Hauptordner: python -m tests.test_hilfen
import builtins
from pathlib import Path

from src.hilfen import (baue_rapport_dateiname, berechne_abgabetermin,
                        behalte_eintraege_des_monats,
                        berechne_arbeitszeit_min,
                        filtere_eintraege_nach_monat, frage_ja_nein,
                        hat_eintrag_fuer_datum, lies_eingabe,
                        sortiere_eintraege_nach_datum,
                        ist_dezimalzahl, ist_gueltige_uhrzeit,
                        ist_gueltiger_monat, ist_gueltiges_datum,
                        ist_nur_ziffern, lese_zeilen_aus_datei,
                        schreibe_zeilen_in_datei, wandle_minuten_in_text_um,
                        wandle_zeit_in_minuten_um, zaehle_tage_im_monat)

# US-04: Datum
assert ist_gueltiges_datum("05.10.2026")
assert not ist_gueltiges_datum("31.02.2026")
assert not ist_gueltiges_datum("5.10.26")
assert not ist_gueltiges_datum("abc")
assert ist_gueltiges_datum("29.02.2028")  # Schaltjahr
assert not ist_gueltiges_datum("29.02.2026")

# US-04: Uhrzeit
assert ist_gueltige_uhrzeit("07:30")
assert ist_gueltige_uhrzeit("23:59")
assert not ist_gueltige_uhrzeit("7:30")
assert not ist_gueltige_uhrzeit("24:00")
assert not ist_gueltige_uhrzeit("25:00")
assert not ist_gueltige_uhrzeit("abc")

# US-07: Monat
assert ist_gueltiger_monat("10.2026")
assert not ist_gueltiger_monat("13.2026")
assert not ist_gueltiger_monat("00.2026")
assert not ist_gueltiger_monat("2026")
assert not ist_gueltiger_monat("abc")

# Zahlen als Text
assert ist_nur_ziffern("45")
assert not ist_nur_ziffern("")
assert not ist_nur_ziffern("4.5")
assert not ist_nur_ziffern("-5")
assert ist_dezimalzahl("32.50")
assert ist_dezimalzahl("5")
assert not ist_dezimalzahl("32,50")
assert not ist_dezimalzahl("abc")
assert not ist_dezimalzahl("")

# Tage im Monat
assert zaehle_tage_im_monat(2, 2026) == 28
assert zaehle_tage_im_monat(2, 2028) == 29
assert zaehle_tage_im_monat(2, 2100) == 28
assert zaehle_tage_im_monat(4, 2026) == 30
assert zaehle_tage_im_monat(10, 2026) == 31

# Zeit und Dauer umwandeln
assert wandle_zeit_in_minuten_um("07:30") == 450
assert wandle_minuten_in_text_um(525) == "8 Std 45 Min"
assert wandle_minuten_in_text_um(0) == "0 Std 00 Min"
eintrag = {"datum": "05.10.2026", "start": "07:30", "ende": "17:00",
           "pause_min": 45}
assert berechne_arbeitszeit_min(eintrag) == 525

# Abgabetermin ist der letzte Tag des Monats
assert berechne_abgabetermin("10.2026") == "31.10.2026"
assert berechne_abgabetermin("11.2026") == "30.11.2026"
assert berechne_abgabetermin("12.2026") == "31.12.2026"
assert berechne_abgabetermin("02.2026") == "28.02.2026"
assert berechne_abgabetermin("02.2028") == "29.02.2028"

# Dateiname des Rapports
assert baue_rapport_dateiname("10.2026") == "rapport_10_2026.txt"

# Einträge eines Monats, nach Datum sortiert
eintraege = [
    {"datum": "12.11.2026", "start": "08:00", "ende": "17:00",
     "pause_min": 60},
    {"datum": "06.10.2026", "start": "08:00", "ende": "16:00",
     "pause_min": 30},
    {"datum": "05.10.2026", "start": "07:30", "ende": "17:00",
     "pause_min": 45},
]
oktober = filtere_eintraege_nach_monat(eintraege, "10.2026")
assert [e["datum"] for e in oktober] == ["05.10.2026", "06.10.2026"]
assert filtere_eintraege_nach_monat(eintraege, "09.2026") == []

# Gibt es das Datum schon?
assert hat_eintrag_fuer_datum(eintraege, "05.10.2026")
assert not hat_eintrag_fuer_datum(eintraege, "07.10.2026")


# Dateien lesen und schreiben: fehlende Datei, fehlender Ordner, kaputte
# Zeichen. Nichts davon darf die App zum Absturz bringen.
TESTDATEN = Path(__file__).resolve().parent / "testdaten"
NEUER_ORDNER = TESTDATEN / "neuer_ordner_test"
DATEI = NEUER_ORDNER / "datei_test.txt"

# Fehlende Datei gibt None statt eines Absturzes
assert lese_zeilen_aus_datei(TESTDATEN / "gibt_es_nicht.txt") is None

# Schreiben legt einen fehlenden Ordner an und gibt True zurück
assert not NEUER_ORDNER.exists()
assert schreibe_zeilen_in_datei(DATEI, ["a;1", "b;2"])
assert DATEI.exists()
assert lese_zeilen_aus_datei(DATEI) == ["a;1\n", "b;2\n"]

# Kaputte Zeichen werden zu ?, die Datei lässt sich trotzdem lesen
DATEI.write_bytes(b"gut\n\xff\xfe\x00schlecht\n")
zeilen = lese_zeilen_aus_datei(DATEI)
assert zeilen[0] == "gut\n"
assert "?" in zeilen[1]

# Schreiben in einen Pfad, der ein Ordner ist, gibt False statt Absturz
assert not schreibe_zeilen_in_datei(NEUER_ORDNER, ["x"])

DATEI.unlink()
NEUER_ORDNER.rmdir()


# Eingaben: Leerzeichen am Rand zählen nicht, j/n auch gross
EINGABEN = []


def fake_input(frage=""):
    """Ersetzt input(): gibt die vorbereiteten Eingaben nacheinander."""
    return EINGABEN.pop(0)


builtins.input = fake_input

EINGABEN.extend(["  6  "])
assert lies_eingabe("Wahl: ") == "6"
EINGABEN.extend([" J "])
assert frage_ja_nein("Sicher?") is True
EINGABEN.extend(["x", "", " N"])
assert frage_ja_nein("Sicher?") is False
assert EINGABEN == []

# Einträge eines Monats behalten und nach Datum sortieren
durcheinander = [
    {"datum": "09.10.2026", "start": "08:00", "ende": "16:00",
     "pause_min": 30},
    {"datum": "05.10.2026", "start": "08:00", "ende": "16:00",
     "pause_min": 30},
    {"datum": "03.11.2026", "start": "08:00", "ende": "16:00",
     "pause_min": 30},
]
nur_oktober = behalte_eintraege_des_monats(durcheinander, "10.2026")
assert len(nur_oktober) == 2
sortiert = sortiere_eintraege_nach_datum(nur_oktober)
assert [e["datum"] for e in sortiert] == ["05.10.2026", "09.10.2026"]

# Eine Datei mit BOM (z. B. von Notepad) verliert keine Zeile
NEUER_ORDNER.mkdir()
DATEI.write_bytes(b"\xef\xbb\xbf05.10.2026;07:30;17:00;45\n")
assert lese_zeilen_aus_datei(DATEI) == ["05.10.2026;07:30;17:00;45\n"]
DATEI.unlink()
NEUER_ORDNER.rmdir()

print("Alle Tests bestanden")
