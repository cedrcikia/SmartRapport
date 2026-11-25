# erinnerung.py · Person B · Erinnerung an den Abgabetermin (US-09)

from src.hilfen import baue_rapport_pfad, berechne_abgabetermin
from src.pfade import DATEN_ORDNER

# Index 0 = Januar, darum später heute.month - 1
MONATSNAMEN = ["Januar", "Februar", "März", "April", "Mai", "Juni",
               "Juli", "August", "September", "Oktober", "November",
               "Dezember"]


def baue_tage_text(tage):
    """Einzahl bei 1, sonst Mehrzahl (auch "0 Tage")."""
    if tage == 1:
        return "noch 1 Tag"
    return f"noch {tage} Tage"


def baue_erinnerung_text(heute, rapport_ordner=DATEN_ORDNER):
    """Gibt den Hinweis als Text zurück, oder "" wenn keiner nötig ist.
    Eigene Funktion, damit man sie mit jedem Datum testen kann.
    """
    # aktueller Monat im Format MM.JJJJ, z. B. "10.2026"
    monat = f"{heute.month:02d}.{heute.year}"
    termin = berechne_abgabetermin(monat)

    # Tage bis zum Abgabetag: der Tag steht vorne im Termin ("31")
    noch = int(termin[0:2]) - heute.day

    # nur in den letzten 4 Tagen (3 Tage vorher bis und mit Abgabetag)
    if noch > 3:
        return ""
    # Rapport schon gespeichert: keine Erinnerung
    if baue_rapport_pfad(monat, rapport_ordner).exists():
        return ""

    name = MONATSNAMEN[heute.month - 1]
    return (f"Rapport {name} bis {termin} abgeben – "
            f"{baue_tage_text(noch)}")


def zeige_erinnerung(heute):
    """US-09: zeigt beim Start den Hinweis oder nichts.
    heute ist ein date-Objekt, so lässt sich jeder Tag testen.
    """
    text = baue_erinnerung_text(heute)
    if text != "":
        print(text)
