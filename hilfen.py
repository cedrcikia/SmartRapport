# hilfen.py · Person A · Hilfsfunktionen für das ganze Team


def preis_zu_rappen(preis):
    """Wandelt einen Preis als Text in ganze Rappen um.
    Beispiel: "12.50" ergibt 1250.
    """
    preis_zahl = float(preis)
    rappen = round(preis_zahl * 100)
    return rappen
