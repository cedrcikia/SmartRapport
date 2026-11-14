# erinnerung.py · Person B · Erinnerung an den Abgabetermin (US-09)

from pathlib import Path

from hilfen import abgabetermin, rapport_dateiname

# Index 0 = Januar, darum später heute.month - 1
MONATSNAMEN = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
               "August", "September", "Oktober", "November", "Dezember"]


def erinnerung_text(heute):
    """Gibt den Hinweis als Text zurück, oder "" wenn keiner nötig ist.
    Eigene Funktion, damit man sie mit jedem Datum testen kann."""
    # aktueller Monat im Format MM.JJJJ, z. B. "10.2026"
    monat = f"{heute.month:02d}.{heute.year}"
    termin = abgabetermin(monat)

    # Tage bis zum Abgabetag: der Tag steht vorne im Termin ("31")
    noch = int(termin[0:2]) - heute.day

    # nur in den letzten 4 Tagen (3 Tage vorher bis und mit Abgabetag)
    if noch > 3:
        return ""
    # Rapport schon gespeichert: keine Erinnerung
    if Path(rapport_dateiname(monat)).exists():
        return ""

    # Einzahl bei 1, sonst Mehrzahl (auch "0 Tage")
    if noch == 1:
        tage_text = "noch 1 Tag"
    else:
        tage_text = f"noch {noch} Tage"
    name = MONATSNAMEN[heute.month - 1]
    return f"Rapport {name} bis {termin} abgeben – {tage_text}"


def pruefe_erinnerung(heute):
    """US-09: zeigt beim Start den Hinweis oder nichts.
    heute ist ein date-Objekt, so lässt sich jeder Tag testen."""
    text = erinnerung_text(heute)
    if text != "":
        print(text)
