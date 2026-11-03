# hilfen.py · Person A · Hilfsfunktionen für das ganze Team


def preis_zu_rappen(preis):
    """Wandelt einen Preis als Text, z.B. "12.50", in ganze Rappen um, z.B. 1250."""
    preis_zahl = float(preis)
    rappen = round(preis_zahl * 100)
    return rappen