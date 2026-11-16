# SmartRapport – Teamplan (intern)

Interne Arbeitsgrundlage für das Team. Gehört nicht zur Abgabe der User Stories. Fachliche Regeln und Stories stehen im `README.md`.

| Person | Name | Stories | Dateien |
|---|---|---|---|
| **A** | Cédric Kialunda | US-01, US-02, US-03 | `src/hilfen.py`, `src/einstellungen.py`, `src/pfade.py` |
| **B** | Leonard Qelaj | US-04, US-05, US-09, Hauptmenü | `src/erfassung.py`, `src/erinnerung.py`, `main.py` |
| **C** | Bledi Isufi | US-06, US-07, US-08 | `src/speicher.py`, `src/verwaltung.py` |
| **D** | Rafaa El Sherkasi | US-10, US-11, US-12 | `src/berechnung.py`, `src/rapport.py` |

---

## Projektstruktur

```
SmartRapport/
├── main.py                 # Start der App und Hauptmenü
├── README.md
├── src/                    # der ganze Programmcode
│   ├── berechnung.py       # Überstunden, Lohn, Übersicht (US-10, US-11)
│   ├── einstellungen.py    # Stundenlohn, Sollzeit, Zuschlag, Abzüge (US-01 bis US-03)
│   ├── erfassung.py        # Arbeitstag und Pause eintragen (US-04, US-05)
│   ├── erinnerung.py       # Erinnerung an den Abgabetermin (US-09)
│   ├── hilfen.py           # gemeinsame Hilfsfunktionen
│   ├── pfade.py            # Speicherorte der Dateien
│   ├── rapport.py          # Rapport als Textdatei (US-12)
│   ├── speicher.py         # Einträge speichern und laden (US-06)
│   └── verwaltung.py       # Einträge anzeigen, ändern, löschen (US-07, US-08)
├── tests/                  # automatische Tests
│   ├── alle_tests.py       # startet alle Tests
│   ├── test_*.py
│   └── testdaten/          # Beispieldateien für die Tests
├── daten/                  # wird von der App angelegt (stunden.txt, einstellungen.txt, Rapporte)
└── docs/
    └── teamplan.md         # diese Datei
```

Der Ordner `daten/` kommt nicht ins Git (siehe `.gitignore`). So landen die echten Stunden nicht im Repository.

---

## Regeln, damit wir parallel arbeiten können

1. **Jede Person bearbeitet nur ihre eigenen Dateien.** Nur so gibt es keine Konflikte in Git. `main.py` gehört B. Wer etwas im Menü braucht, sagt es B.
2. **Die Funktionsnamen unten sind fix.** Sie sind unser Vertrag. Namen, Parameter und Rückgabewerte ändern wir nur gemeinsam im Team.
3. **Niemand wartet auf andere.** Jede Person testet mit den Testdaten und den Tests.
4. **Regelmässig committen, mit eigenem Namen.** Die Dozierenden prüfen die Beiträge über die Commits.
5. **Jede Zeile erklären können.** Bei jeder Funktion steht ein Kommentar in eigenen Worten. In der Fragerunde muss jede Person ihren Code Zeile für Zeile erklären können (Projektrichtlinien, Kap. 4 und 6).
6. **KI-Nutzung deklarieren.** KI darf helfen (Debuggen, Erklären, Sparring), muss aber angegeben werden. KI-generierte Projekte werden nicht akzeptiert.
7. **Vor jeder Arbeit `git pull`, nach jeder Änderung bald committen und pushen.** So gibt es weniger Merge-Konflikte.

---

## Namensregeln

* **Jede Funktion beginnt mit einem Verb**, das sagt, was sie macht: `lade_`, `speichere_`, `zeige_`, `frage_`, `berechne_`, `baue_`, `wandle_..._um`, `filtere_`, `aendere_`, `loesche_`, `waehle_`, `trage_..._ein`, `zaehle_`, `lege_..._an`, `starte_`. Funktionen, die `True` oder `False` zurückgeben, beginnen mit `ist_` oder `hat_`.
* **Variablen und Konstanten sind Nomen.** Konstanten schreiben wir GROSS (`STUNDEN_DATEI`).
* **Minuten als Zahl** enden auf `_min` (`arbeits_min`, `soll_min`, `pause_min`).
* **`monat`** ist immer der Text `"10.2026"`, **`monat_nummer`** ist die Zahl 10.
* **`eintraege`** ist die Liste aller Einträge, **`monats_eintraege`** die Einträge eines Monats, **`eintrag`** ein einzelner.
* **`eingabe`** ist das, was die Person getippt hat.
* Schlüssel in Dictionaries sind klein geschrieben (`"ahv"`, nicht `"AHV"`).

---

## Gemeinsame Datenformen

**Ein Eintrag** (Dictionary mit den Schlüsseln `datum`, `start`, `ende`, `pause_min`), z.B.:

```
{"datum": "05.10.2026", "start": "07:30", "ende": "17:00", "pause_min": 45}
```

`pause_min` ist eine Zahl (`int`), alles andere ist Text (`str`).

**Alle Einträge** sind eine Liste (`list`) solcher Dictionaries. Pro Datum gibt es höchstens einen Eintrag.

**Einstellungen** (Dictionary), z.B.:

```
{"stundenlohn": 32.5, "soll_min": 480, "zuschlag": 25.0, "ahv": 5.3, "alv": 1.1, "nbu": 3.74}
```

**Monat** ist immer ein Text im Format `"10.2026"`.

**Ergebnis der Berechnung** (Dictionary, das D liefert):

```
{"normal_min": 930, "ueber_min": 45, "brutto": 534.22,
 "abzuege": {"ahv": 28.31, "alv": 5.88, "nbu": 19.98}, "netto": 480.05}
```

---

## Schnittstellen (die Funktionen, die wir einander anbieten)

### `src/pfade.py` (Person A)

| Name | Zweck |
|---|---|
| `PROJEKT_ORDNER`, `DATEN_ORDNER` | Hauptordner und Ordner `daten/` |
| `STUNDEN_DATEI`, `EINSTELLUNGEN_DATEI` | Pfade von `stunden.txt` und `einstellungen.txt` im Ordner `daten/` |
| `lege_daten_ordner_an()` | legt `daten/` an, falls er fehlt |

### `src/hilfen.py` (Person A)

| Funktion | Gibt zurück | Zweck |
|---|---|---|
| `ist_nur_ziffern(text)` | `True`/`False` | nicht leer und nur Ziffern |
| `ist_dezimalzahl(text)` | `True`/`False` | Zahl wie `32.50` oder `5`, Komma ist ungültig |
| `ist_gueltiges_datum(text)` | `True`/`False` | prüft `TT.MM.JJJJ` und ob das Datum existiert |
| `ist_gueltige_uhrzeit(text)` | `True`/`False` | prüft `HH:MM` von `00:00` bis `23:59` |
| `ist_gueltiger_monat(text)` | `True`/`False` | prüft `MM.JJJJ` |
| `zaehle_tage_im_monat(monat_nummer, jahr)` | Zahl | Tage des Monats, Februar mit Schaltjahr |
| `wandle_zeit_in_minuten_um(text)` | Zahl | `"07:30"` wird zu `450` |
| `wandle_minuten_in_text_um(gesamt_min)` | Text | `525` wird zu `"8 Std 45 Min"` |
| `berechne_arbeitszeit_min(eintrag)` | Zahl | Ende minus Start minus Pause |
| `filtere_eintraege_nach_monat(eintraege, monat)` | Liste | Einträge dieses Monats, nach Datum sortiert |
| `hat_eintrag_fuer_datum(eintraege, datum)` | `True`/`False` | gibt es für dieses Datum schon einen Eintrag |
| `berechne_abgabetermin(monat)` | Text | `"10.2026"` wird zu `"31.10.2026"` (letzter Tag des Monats) |
| `baue_rapport_dateiname(monat)` | Text | `"10.2026"` wird zu `"rapport_10_2026.txt"` |
| `baue_rapport_pfad(monat, ordner)` | Pfad | voller Pfad des Rapports im Ordner `daten/` |
| `frage_ja_nein(frage)` | `True`/`False` | fragt `j/n`, bis die Eingabe stimmt |
| `frage_monat()` | Text | fragt den Monat, bis er gültig ist |

### `src/einstellungen.py` (Person A)

| Funktion | Zweck |
|---|---|
| `lade_einstellungen(dateiname)` | liest `einstellungen.txt`, legt sie mit Standardwerten an, falls sie fehlt. Gibt das Einstellungs-Dictionary zurück |
| `speichere_einstellungen(einstellungen, dateiname)` | schreibt `einstellungen.txt` |
| `aendere_stundenlohn(einstellungen)` | US-01 |
| `aendere_sollzeit(einstellungen)` | US-02 |
| `frage_prozent(frage)` | fragt einen Prozentwert von 0 bis 100 |
| `aendere_zuschlag_und_abzuege(einstellungen)` | US-03 |

### `src/erfassung.py` (Person B)

| Funktion | Zweck |
|---|---|
| `frage_datum(eintraege)` | fragt ein Datum ab, bis es gültig ist und noch kein Eintrag dafür existiert. Gibt Text zurück |
| `frage_uhrzeit(frage)` | fragt eine Uhrzeit mit dem Fragetext ab, bis sie gültig ist. Gibt Text zurück |
| `frage_pause(max_min)` | fragt die Pause ab, sie muss kürzer als `max_min` sein. Gibt eine Zahl zurück |
| `frage_eintrag(eintraege)` | fragt Datum, Start, Ende und Pause ab und gibt den neuen Eintrag zurück. Wird auch von US-08 gebraucht |
| `trage_arbeitstag_ein(eintraege)` | US-04 und US-05: ruft `frage_eintrag` auf, hängt den Eintrag an die Liste an und speichert |

### `src/erinnerung.py` (Person B)

| Funktion | Zweck |
|---|---|
| `baue_erinnerung_text(heute, rapport_ordner)` | gibt den Hinweis als Text zurück, oder `""`. So lässt sich jeder Tag testen |
| `zeige_erinnerung(heute)` | US-09: zeigt den Hinweis oder nichts. `heute` ist ein `date`-Objekt |

### `src/speicher.py` (Person C)

| Funktion | Zweck |
|---|---|
| `wandle_eintrag_in_zeile_um(eintrag)` | `{"datum": ...}` wird zu `"05.10.2026;07:30;17:00;45"` |
| `ist_gueltige_zeile(felder)` | prüft, ob die 4 Felder einer Zeile gültig sind (wie bei US-04 und US-05) |
| `lade_eintraege(dateiname)` | US-06: liest `stunden.txt`, überspringt kaputte Zeilen und doppelte Daten mit Meldung. Gibt die Liste der Einträge zurück |
| `speichere_eintraege(eintraege, dateiname)` | schreibt die ganze Liste in `stunden.txt` |

### `src/verwaltung.py` (Person C)

| Funktion | Zweck |
|---|---|
| `zeige_liste(monats_eintraege)` | zeigt die Einträge nummeriert ab 1 mit Total |
| `zeige_eintraege(eintraege)` | US-07: fragt den Monat ab und zeigt die Liste |
| `waehle_eintrag(monats_eintraege)` | fragt die Nummer, bis sie gültig ist, und gibt den Eintrag zurück |
| `aendere_eintrag(eintraege, eintrag)` | US-08: neue Werte abfragen (mit `frage_eintrag`), speichern |
| `loesche_eintrag(eintraege, eintrag)` | US-08: nach Rückfrage löschen, speichern |
| `aendere_oder_loesche_eintrag(eintraege)` | US-08: Monat, Nummer und `1` ändern oder `2` löschen |

### `src/berechnung.py` (Person D)

| Funktion | Zweck |
|---|---|
| `berechne_ueberstunden(monats_eintraege, soll_min)` | US-10: zählt pro Tag Normalstunden und Überstunden (in Minuten) und summiert sie über den Monat. Gibt `(normal_min, ueber_min)` zurück |
| `berechne_monat(monats_eintraege, einstellungen)` | US-10 und Lohn: ruft `berechne_ueberstunden` auf und gibt das Ergebnis-Dictionary zurück |
| `baue_zeile(bezeichnung, wert)` | eine Zeile der Übersicht mit fester Spaltenbreite |
| `baue_uebersicht_zeilen(ergebnis, einstellungen)` | US-11 und US-12: baut die Zeilen der Lohnübersicht als Liste. So sind die Beträge in der Übersicht und im Rapport gleich |
| `zeige_uebersicht(eintraege, einstellungen)` | US-11: fragt den Monat ab und zeigt die Übersicht |

### `src/rapport.py` (Person D)

| Funktion | Zweck |
|---|---|
| `baue_eintragszeilen(monats_eintraege)` | US-12: eine Zeile pro Eintrag (ab 1 nummeriert, wie in US-07) und am Schluss das Total |
| `baue_rapport(monat, monats_eintraege, einstellungen)` | US-12: setzt alle Zeilen des Rapports zusammen, ohne eine Datei zu schreiben |
| `speichere_rapport(eintraege, einstellungen)` | US-12: fragt den Monat ab, fragt bei bestehender Datei nach und schreibt `rapport_MM_JJJJ.txt` in den Ordner `daten/` |

### `main.py` (Person B)

Ablauf beim Start: `lege_daten_ordner_an()` → `lade_einstellungen()` → `lade_eintraege()` → `zeige_erinnerung(heute)` → Hauptmenü (Festlegung 8 im README).

| Menüpunkt | Ruft auf | Von |
|---|---|---|
| 1 Arbeitstag eintragen | `trage_arbeitstag_ein(eintraege)` | B |
| 2 Einträge anzeigen | `zeige_eintraege(eintraege)` | C |
| 3 Eintrag ändern oder löschen | `aendere_oder_loesche_eintrag(eintraege)` | C |
| 4 Übersicht anzeigen | `zeige_uebersicht(eintraege, einstellungen)` | D |
| 5 Rapport speichern | `speichere_rapport(eintraege, einstellungen)` | D |
| 6 Stundenlohn ändern | `aendere_stundenlohn(einstellungen)` | A |
| 7 Sollzeit ändern | `aendere_sollzeit(einstellungen)` | A |
| 8 Zuschlag und Abzüge ändern | `aendere_zuschlag_und_abzuege(einstellungen)` | A |
| 9 Beenden | `Auf Wiedersehen!` und Programmende | B |

---

## Tests

Alle Tests liegen im Ordner `tests/` und werden im Hauptordner gestartet:

```
python -m tests.alle_tests
```

Ein einzelner Test, z.B. `python -m tests.test_berechnung`. Die Beispieldateien liegen in `tests/testdaten/` (`stunden_beispiel.txt` mit 3 gültigen Zeilen, `stunden_fehler.txt` mit einer kaputten Zeile und einem doppelten Datum). Mit `stunden_beispiel.txt` ist das erwartete Ergebnis für den Monat `10.2026` bekannt: 15 Std 30 Min normal, 0 Std 45 Min Überstunden, Brutto CHF 534.22, AHV CHF 28.31, ALV CHF 5.88, NBU CHF 19.98, Netto CHF 480.05.

---
## Zeitplan (an das Semesterprogramm angepasst)

| Bis wann | Unser Ziel | Meilenstein laut Semesterprogramm |
|---|---|---|
| So 11.10. | User Stories fertig und auf Moodle abgegeben (Frist: 12.10., 00:00) | KW 41: User Stories definiert und hochgeladen |
| So 18.10. | Repository mit allen leeren Dateien und Funktionsnamen, Testdaten im Repo. Funktionsbaum und Ablaufskizze für `main.py`. A liefert `hilfen.py` | KW 42: Haupt-Entscheidungs- und Kontrollfluss definiert |
| So 25.10. | Jede Person: Kernfunktionen laufen einzeln mit Testdaten, inkl. ungültiger Eingaben | KW 43: Programmfluss und Kernfunktionen umgesetzt · KW 44: Haupt- und Alternativabläufe umgesetzt, Kernfunktionen getestet |
| So 15.11. | Zusammensetzen in `main.py`. Lesen und Schreiben der Dateien funktioniert, kein Absturz bei fehlenden oder kaputten Dateien | KW 47: Datei-Ein- und Ausgabe und Exception Handling umgesetzt |
| So 22.11. | Alle Akzeptanzkriterien gemeinsam durchspielen, Validierung vollständig | KW 48: Datenvalidierung und Exception Handling umgesetzt |
| So 29.11. | Fehler beheben, README fertig (Anforderungen, Implementation, Beiträge), Folien | KW 49: vollständige Anwendung |
| So 6.12., 23:55 | Abgabe: PDF der Folien mit Link zum **öffentlichen** Repo | Abgabe 6.12., 23:55 |

Die Präsentation (15 Minuten, alle sprechen) findet in den letzten beiden Semesterwochen statt.

---

## Wenn jemand früher fertig ist oder nicht weiterkommt

* **A früher fertig:** übernimmt Tests für alle (die Beispiele aus den Akzeptanzkriterien nachspielen), die README-Abschnitte Anforderungen und Libraries und hilft D.
* **D kommt nicht weiter:** A oder B übernimmt US-11 (Übersicht). Das ist nur Anzeige, wenn `berechne_monat` schon das Ergebnis liefert. Früh im Team melden, weil die Beiträge in Git sichtbar sein müssen.

---

## Entscheidungen im Team (11.10.2026)

1. **Pro Datum höchstens ein Eintrag** (Festlegung 2, US-04, US-06, US-08).
2. **Abgabetermin = letzter Tag des Monats** (Festlegung 6, US-09, US-12).
3. **Nur der Punkt als Dezimaltrennzeichen** (Festlegung 5).
4. **NBU-Satz 3.74 %** in allen Beispielen und als Standardwert (Festlegung 7).
5. **Auszahlung am 5. des Folgemonats** steht nur im Szenario, wird nicht programmiert.
6. **Clean-up (16.11.2026):** Ordnerstruktur (`src/`, `tests/`, `daten/`, `docs/`), jede Funktion beginnt mit einem Verb, doppelte Funktionen nur noch in `src/hilfen.py`, einheitliche Namen (siehe Namensregeln).
