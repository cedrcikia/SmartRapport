from hilfen import (arbeitszeit_minuten, eintraege_des_monats, frage_monat,
                    minuten_zu_text)


def zeige_eintraege(eintraege):
    monat = frage_monat()
    gefunden = eintraege_des_monats(eintraege, monat)
    if len(gefunden) == 0:
        print(f"Keine Einträge für {monat}.")
    else:
        nummer = 0 
        total = 0
        for eintrag in gefunden:
            nummer += 1
            datum = eintrag["datum"]
            start = eintrag["start"]
            ende = eintrag["ende"]
            pause = eintrag["pause_min"]
            minuten = arbeitszeit_minuten(eintrag)

            print(f"{nummer}. {datum}  {start}–{ende}  Pause {pause} Min  {minuten_zu_text(minuten)}")
            total += minuten    
        print(f"Total: {minuten_zu_text(total)}")
