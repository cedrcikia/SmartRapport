# main.py · Person B · Hauptmenü von SmartRapport (Festlegung 8)
# Start der App: python main.py

from datetime import date

from src.berechnung import zeige_uebersicht
from src.einstellungen import (aendere_sollzeit, aendere_stundenlohn,
                               aendere_zuschlag_und_abzuege,
                               lade_einstellungen)
from src.erfassung import trage_arbeitstag_ein
from src.erinnerung import zeige_erinnerung
from src.hilfen import lies_eingabe
from src.pfade import lege_daten_ordner_an
from src.rapport import speichere_rapport
from src.speicher import lade_eintraege
from src.verwaltung import aendere_oder_loesche_eintrag, zeige_eintraege


def zeige_hauptmenue():
    """Zeigt das Hauptmenü mit den Punkten 1 bis 9."""
    print()
    print("[SMARTRAPPORT - HAUPTMENÜ]")
    print("1. Arbeitstag eintragen")
    print("2. Einträge anzeigen")
    print("3. Eintrag ändern oder löschen")
    print("4. Übersicht anzeigen")
    print("5. Rapport speichern")
    print("6. Stundenlohn ändern")
    print("7. Sollzeit ändern")
    print("8. Zuschlag und Abzüge ändern")
    print("9. Beenden")


def fuehre_eintragsfunktion_aus(wahl, eintraege, einstellungen):
    """Führt Menüpunkt 1 bis 5 aus (Einträge, Übersicht, Rapport)."""
    if wahl == "1":
        trage_arbeitstag_ein(eintraege)
    elif wahl == "2":
        zeige_eintraege(eintraege)
    elif wahl == "3":
        aendere_oder_loesche_eintrag(eintraege)
    elif wahl == "4":
        zeige_uebersicht(eintraege, einstellungen)
    else:
        speichere_rapport(eintraege, einstellungen)


def fuehre_einstellungsfunktion_aus(wahl, einstellungen):
    """Führt Menüpunkt 6 bis 8 aus (Stundenlohn, Sollzeit, Sätze)."""
    if wahl == "6":
        aendere_stundenlohn(einstellungen)
    elif wahl == "7":
        aendere_sollzeit(einstellungen)
    else:
        aendere_zuschlag_und_abzuege(einstellungen)


def fuehre_menuepunkt_aus(wahl, eintraege, einstellungen):
    """Führt den gewählten Menüpunkt aus. Gibt False zurück bei 9
    (Beenden), sonst True.
    """
    if wahl in ("1", "2", "3", "4", "5"):
        fuehre_eintragsfunktion_aus(wahl, eintraege, einstellungen)
    elif wahl in ("6", "7", "8"):
        fuehre_einstellungsfunktion_aus(wahl, einstellungen)
    elif wahl == "9":
        # alles wurde schon beim Ändern gespeichert, darum nur Abschied
        print("Auf Wiedersehen!")
        return False
    else:
        # 0, 10, abc oder leer
        print("Ungültige Wahl.")
    return True


def lade_startdaten():
    """Legt den Ordner daten/ an, lädt Einstellungen und Einträge
    (Festlegung 7) und erinnert an den Abgabetermin (US-09).
    """
    lege_daten_ordner_an()
    einstellungen = lade_einstellungen()
    eintraege = lade_eintraege()
    zeige_erinnerung(date.today())
    return einstellungen, eintraege


def starte_app():
    """Startablauf laut Teamplan, dann Hauptmenü, bis der Benutzer 9
    wählt.
    """
    einstellungen, eintraege = lade_startdaten()

    # Das Menü erscheint nach jeder Funktion wieder. Strg+C und Strg+Z
    # (Eingabe-Ende) beenden die App ohne Fehlermeldung. Gespeichert
    # wird schon bei jeder Änderung, es geht nichts verloren.
    weiter = True
    try:
        while weiter:
            zeige_hauptmenue()
            wahl = lies_eingabe("Deine Wahl: ")
            weiter = fuehre_menuepunkt_aus(wahl, eintraege, einstellungen)
    except KeyboardInterrupt:
        print()
        print("Programm beendet.")
    except EOFError:
        print()
        print("Programm beendet.")


# Startet das Menü nur, wenn main.py direkt ausgeführt wird
if __name__ == "__main__":
    starte_app()
