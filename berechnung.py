# berechnung.py · Person D · Überstunden und Lohn eines Monats (US-10, US-11)

from hilfen import (arbeitszeit_minuten, eintraege_des_monats, frage_monat,
                    minuten_zu_text)


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


def baue_uebersicht_zeilen(ergebnis, einstellungen):
    """Baut die Zeilen der Lohnübersicht. US-11 und US-12 nutzen sie
    beide, so sind die Beträge überall gleich.
    """
    abzuege = ergebnis["abzuege"]
    normal = minuten_zu_text(ergebnis["normal_min"])
    ueber = minuten_zu_text(ergebnis["ueber_min"])
    zeilen = []
    zeilen.append(f"{'Normalstunden:':<19}{normal:>13}")
    zeilen.append(f"{'Überstunden:':<19}{ueber:>13}")
    zeilen.append(f"{'Brutto:':<19}CHF {ergebnis['brutto']:.2f}")
    # Der Prozentsatz im Text kommt aus den Einstellungen, nicht fest
    for name in ("AHV", "ALV", "NBU"):
        satz = einstellungen[name.lower()]
        text = f"{name} ({satz:.2f} %):"
        zeilen.append(f"{text:<19}-CHF {abzuege[name]:.2f}")
    zeilen.append(f"{'Netto:':<19}CHF {ergebnis['netto']:.2f}")
    return zeilen


def zeige_uebersicht(eintraege, einstellungen):
    """US-11: Fragt den Monat ab und zeigt Stunden, Lohn und Abzüge."""
    monat = frage_monat()
    monats_eintraege = eintraege_des_monats(eintraege, monat)
    # Ohne Einträge gibt es nichts zu rechnen, also gleich beenden
    if len(monats_eintraege) == 0:
        print(f"Keine Einträge für {monat}.")
        return
    ergebnis = berechne_monat(monats_eintraege, einstellungen)
    for zeile in baue_uebersicht_zeilen(ergebnis, einstellungen):
        print(zeile)
