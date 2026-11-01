def eintraege_des_monats(eintraege, monat): 
    gefunden = []
    for eintrag in eintraege:
        datum = eintrag["datum"]
        if datum[3:] == monat:
            gefunden.append(eintrag)
    return gefunden
