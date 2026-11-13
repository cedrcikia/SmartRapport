# speicher.py · Person C · US-06 Einträge speichern und laden


def eintrag_zu_zeile(eintrag):
    """Wandelt einen Eintrag in eine Zeile für stunden.txt um.

    Story: US-06 (Teil: Processing)

    Parameter:
        eintrag (dict): Ein Eintrag mit datum, start, ende und
            pause_min, z. B. {"datum": "05.10.2026",
            "start": "07:30", "ende": "17:00", "pause_min": 45}

    Rückgabe:
        str: Zeile im Format Datum;Start;Ende;Pause,
        z. B. "05.10.2026;07:30;17:00;45"

    Wird aufgerufen von: speichere_eintraege
    """
    datum = eintrag["datum"]
    start = eintrag["start"]
    ende = eintrag["ende"]
    pause = eintrag["pause_min"]
    return f"{datum};{start};{ende};{pause}"

