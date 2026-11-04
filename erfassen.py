# erfassen.py · Person B · Arbeitstag und Pause erfassen (US-04, US-05)

# Testwert aus README, kommt später von US-04
dauer = 570

# US-05: so lange fragen, bis die Pause gültig ist (Schleife)
while True:
    pause = input("Pause in Minuten: ")

    # kein Zeichen ist leere Eingabe, deshalb separat prüfen
    gueltig = True
    if pause == "":
        gueltig = False

    # nur ganze Zahlen erlaubt; -5, 4.5 und abc fallen weg
    for zeichen in pause:
        if zeichen not in "0123456789":
            gueltig = False

    # int() erst hier: ungültige Eingaben kommen gar nicht so weit
    if gueltig == False:
        print("Ungültige Pause.")
    elif int(pause) >= dauer:
        print("Die Pause muss kürzer sein als die Zeit",
              "zwischen Start und Ende.")
    else:
        break

# Arbeitszeit = Zeit zwischen Start und Ende minus Pause
arbeit_min = dauer - int(pause)
stunden = arbeit_min // 60
minuten = arbeit_min % 60
print(f"Arbeitszeit: {stunden} Std {minuten:02d} Min")
