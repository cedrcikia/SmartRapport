# berechnung.py · Person D · Überstunden und Lohn eines Monats (US-10)

from hilfen import arbeitszeit_minuten


def berechne_ueberstunden(monats_eintraege, soll_min):
    """US-10: Zählt pro Tag Normalstunden und Überstunden (in Minuten)
    und summiert sie über den Monat.
    """
    # Beide Summen starten bei 0, bei einem leeren Monat bleibt es dabei
    normal_min = 0
    ueber_min = 0
    for eintrag in monats_eintraege:
        arbeits_min = arbeitszeit_minuten(eintrag)
        # Normal ist höchstens die Sollzeit, der Rest eines Tages ist Überzeit
        normal_min += min(arbeits_min, soll_min)
        # Bei weniger als der Sollzeit wäre die Differenz negativ,
        # darum max(0, ...): dann gibt es 0 Überstunden
        ueber_min += max(0, arbeits_min - soll_min)
    return normal_min, ueber_min


def berechne_monat(monats_eintraege, einstellungen):
    """Berechnet Stunden, Bruttolohn, Abzüge und Nettolohn eines Monats."""
    normal_min, ueber_min = berechne_ueberstunden(
        monats_eintraege, einstellungen["soll_min"])
    normal_lohn = normal_min / 60 * einstellungen["stundenlohn"]
    ueber_lohn = (ueber_min / 60 * einstellungen["stundenlohn"]
                  * (1 + einstellungen["zuschlag"] / 100))
    # Zuerst Brutto auf 2 Stellen runden, die Abzüge rechnen dann damit
    brutto = round(normal_lohn + ueber_lohn, 2)
    abzuege = {}
    for name in ("ahv", "alv", "nbu"):
        abzuege[name.upper()] = round(brutto * einstellungen[name] / 100, 2)
    netto = round(brutto - sum(abzuege.values()), 2)
    return {"normal_min": normal_min, "ueber_min": ueber_min,
            "brutto": brutto, "abzuege": abzuege, "netto": netto}
