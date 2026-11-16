# pfade.py · Speicherorte aller Dateien der App (an einem Ort)

import os
from pathlib import Path

# Hauptordner des Projekts: eine Ebene über src/
PROJEKT_ORDNER = Path(__file__).resolve().parent.parent
DATEN_ORDNER = PROJEKT_ORDNER / "daten"
STUNDEN_DATEI = DATEN_ORDNER / "stunden.txt"
EINSTELLUNGEN_DATEI = DATEN_ORDNER / "einstellungen.txt"


def lege_daten_ordner_an():
    """Legt den Ordner daten/ an, falls es ihn noch nicht gibt."""
    os.makedirs(DATEN_ORDNER, exist_ok=True)
