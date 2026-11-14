# SmartRapport – Teamplan (intern)

Interne Arbeitsgrundlage für das Team. Gehört nicht zur Abgabe der User Stories. Fachliche Regeln und Stories stehen im `README.md`.

| Person | Name | Stories | Dateien |
|---|---|---|---|
| **A** | Cédric Kialunda | US-01, US-02, US-03 | `hilfen.py`, `einstellungen.py` |
| **B** | Leonard Qelaj | US-04, US-05, US-09, Hauptmenü | `erfassen.py`, `erinnerung.py`, `main.py` |
| **C** | Bledi Isufi | US-06, US-07, US-08 | `speicher.py`, `verwaltung.py` |
| **D** | Rafaa El Sherkasi | US-10, US-11, US-12 | `berechnung.py`, `rapport.py` |

---

## Regeln, damit wir parallel arbeiten können

1. **Jede Person bearbeitet nur ihre eigenen Dateien.** Nur so gibt es keine Konflikte in Git. `main.py` gehört B. Wer etwas im Menü braucht, sagt es B.
2. **Die Funktionsnamen unten sind fix.** Sie sind unser Vertrag. Namen, Parameter und Rückgabewerte ändern wir nur gemeinsam im Team.
3. **Niemand wartet auf andere.** Jede Person testet zuerst mit Testdaten und kleinen Dummy-Funktionen (siehe unten). Erst wenn alle Teile fertig sind, setzen wir alles zusammen.
4. **Regelmässig committen, mit eigenem Namen.** Die Dozierenden prüfen die Beiträge über die Commits.
5. **Jede Zeile erklären können.** Bei jeder Funktion steht ein Kommentar in eigenen Worten. In der Fragerunde muss jede Person ihren Code Zeile für Zeile erklären können (Projektrichtlinien, Kap. 4 und 6).
6. **KI-Nutzung deklarieren.** KI darf helfen (Debuggen, Erklären, Sparring), muss aber angegeben werden. KI-generierte Projekte werden nicht akzeptiert.

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
 "abzuege": {"AHV": 28.31, "ALV": 5.88, "NBU": 19.98}, "netto": 480.05}
```

---

## Schnittstellen (die Funktionen, die wir einander anbieten)

### `hilfen.py` (Person A)

| Funktion | Gibt zurück | Zweck |
|---|---|---|
| `zeit_zu_minuten(text)` | Zahl | `"07:30"` wird zu `450` |
| `minuten_zu_text(minuten)` | Text | `525` wird zu `"8 Std 45 Min"` |
| `ist_gueltiges_datum(text)` | `True`/`False` | prüft `TT.MM.JJJJ` und ob das Datum existiert |
| `ist_gueltige_uhrzeit(text)` | `True`/`False` | prüft `HH:MM` von `00:00` bis `23:59` |
| `ist_gueltiger_monat(text)` | `True`/`False` | prüft `MM.JJJJ` |
| `frage_monat()` | Text | fragt den Monat ab, bis er gültig ist |
| `frage_ja_nein(frage)` | `True`/`False` | fragt `j/n` ab, bis die Eingabe stimmt |
| `arbeitszeit_minuten(eintrag)` | Zahl | Ende minus Start minus Pause |
| `datum_existiert(eintraege, datum)` | `True`/`False` | prüft, ob es für dieses Datum schon einen Eintrag gibt. Brauchen B (US-04) und C (US-06, US-08) |
| `rapport_dateiname(monat)` | Text | `"10.2026"` wird zu `"rapport_10_2026.txt"`. Brauchen B (US-09) und D (US-12) |
| `abgabetermin(monat)` | Text | `"10.2026"` wird zu `"31.10.2026"` (letzter Tag des Monats). Brauchen B (US-09) und D (US-12) |

### `einstellungen.py` (Person A)

| Funktion | Zweck |
|---|---|
| `lade_einstellungen()` | liest `einstellungen.txt`, legt sie mit Standardwerten an, falls sie fehlt. Gibt das Einstellungs-Dictionary zurück |
| `speichere_einstellungen(einstellungen)` | schreibt `einstellungen.txt` |
| `stundenlohn_eingeben(einstellungen)` | US-01 |
| `sollzeit_eingeben(einstellungen)` | US-02 |
| `saetze_eingeben(einstellungen)` | US-03 |

### `erfassen.py` (Person B)

| Funktion | Zweck |
|---|---|
| `frage_datum(eintraege)` | fragt ein Datum ab, bis es gültig ist und noch kein Eintrag dafür existiert (ruft `datum_existiert` auf). Gibt Text zurück |
| `frage_uhrzeit(text)` | fragt eine Uhrzeit mit dem Fragetext ab. Gibt Text zurück |
| `frage_pause(max_min)` | fragt die Pause ab, sie muss kürzer als `max_min` sein. Gibt eine Zahl zurück |
| `arbeitstag_eintragen(eintraege)` | US-04 und US-05: fragt alles ab, hängt den Eintrag an die Liste an und speichert (ruft `speichere_eintraege` auf) |

### `erinnerung.py` (Person B)

| Funktion | Zweck |
|---|---|
| `pruefe_erinnerung(heute)` | US-09: zeigt den Hinweis oder nichts. `heute` ist ein `date`-Objekt, so lässt sich jeder Tag testen. Nutzt `abgabetermin` und `rapport_dateiname` |

### `speicher.py` (Person C)

| Funktion | Zweck |
|---|---|
| `lade_eintraege()` | US-06: liest `stunden.txt`, überspringt kaputte Zeilen und doppelte Daten mit Meldung. Gibt die Liste der Einträge zurück |
| `speichere_eintraege(eintraege)` | schreibt die ganze Liste in `stunden.txt` |

### `verwaltung.py` (Person C)

| Funktion | Zweck |
|---|---|
| `eintraege_des_monats(eintraege, monat)` | Einträge dieses Monats, nach Datum sortiert. D braucht diese Funktion auch |
| `zeige_eintraege(eintraege)` | US-07: fragt den Monat ab und zeigt die nummerierte Liste mit Total |
| `aendern_loeschen(eintraege)` | US-08: Liste zeigen, Nummer wählen, `1` ändern oder `2` löschen, speichern. Beim Ändern wird das Datum mit `datum_existiert` geprüft |

### `berechnung.py` (Person D)

| Funktion | Zweck |
|---|---|
| `berechne_ueberstunden(monats_eintraege, soll_min)` | US-10: zählt pro Tag Normalstunden und Überstunden (in Minuten) und summiert sie über den Monat. Gibt `(normal_min, ueber_min)` zurück |
| `berechne_monat(monats_eintraege, einstellungen)` | US-10 und Lohn: ruft `berechne_ueberstunden` auf und gibt das Ergebnis-Dictionary zurück |
| `baue_uebersicht_zeilen(ergebnis, einstellungen)` | US-11 und US-12: baut die Zeilen der Lohnübersicht als Liste. So sind die Beträge in der Übersicht und im Rapport gleich |
| `zeige_uebersicht(eintraege, einstellungen)` | US-11: fragt den Monat ab und zeigt die Übersicht |

### `rapport.py` (Person D)

| Funktion | Zweck |
|---|---|
| `baue_eintragszeilen(monats_eintraege)` | US-12: eine Zeile pro Eintrag (ab 1 nummeriert, wie in US-07) und am Schluss das Total. Gibt eine Liste von Zeilen zurück |
| `baue_rapport(monat, monats_eintraege, einstellungen)` | US-12: setzt alle Zeilen des Rapports zusammen (Kopf, Einträge, Lohnübersicht), ohne eine Datei zu schreiben |
| `rapport_speichern(eintraege, einstellungen)` | US-12: fragt den Monat ab, fragt bei bestehender Datei nach und schreibt `rapport_MM_JJJJ.txt` (mit `abgabetermin`) |

### `main.py` (Person B)

Ablauf beim Start: `lade_einstellungen()` → `lade_eintraege()` → `pruefe_erinnerung(heute)` → Hauptmenü (Festlegung 8 im README).

| Menüpunkt | Ruft auf | Von |
|---|---|---|
| 1 Arbeitstag eintragen | `arbeitstag_eintragen(eintraege)` | B |
| 2 Einträge anzeigen | `zeige_eintraege(eintraege)` | C |
| 3 Eintrag ändern oder löschen | `aendern_loeschen(eintraege)` | C |
| 4 Übersicht anzeigen | `zeige_uebersicht(eintraege, einstellungen)` | D |
| 5 Rapport speichern | `rapport_speichern(eintraege, einstellungen)` | D |
| 6 Stundenlohn ändern | `stundenlohn_eingeben(einstellungen)` | A |
| 7 Sollzeit ändern | `sollzeit_eingeben(einstellungen)` | A |
| 8 Zuschlag und Abzüge ändern | `saetze_eingeben(einstellungen)` | A |
| 9 Beenden | `Auf Wiedersehen!` und Programmende | B |

---

## Wie jede Person ohne die anderen anfangen kann

**Testdaten** (liegen im Repo, alle haben dieselben):

`stunden.txt`
```
05.10.2026;07:30;17:00;45
06.10.2026;08:00;16:00;30
12.11.2026;08:00;17:00;60
```

`einstellungen.txt`
```
stundenlohn=32.50
soll_min=480
zuschlag=25
ahv=5.3
alv=1.1
nbu=3.74
```

Mit diesen Daten ist das erwartete Ergebnis für den Monat `10.2026` bekannt: 15 Std 30 Min normal, 0 Std 45 Min Überstunden, Brutto CHF 534.22, AHV CHF 28.31, ALV CHF 5.88, NBU CHF 19.98, Netto CHF 480.05. Das sind die Testfälle für D.

`stunden_fehler.txt` (nur für C, zum Testen von US-06)
```
05.10.2026;07:30;17:00;45
05.10.2026;07:30;abc;45
05.10.2026;08:00;16:00;30
```

Erwartet: Zeile 1 wird geladen, Zeile 2 wird als kaputt übersprungen, Zeile 3 wird wegen doppeltem Datum übersprungen.

**Was jede Person am Anfang tut:**

| Person | Erster Schritt, ohne auf andere zu warten |
|---|---|
| A | `hilfen.py` zuerst, weil alle sie brauchen. Danach `einstellungen.py` |
| B | Die Funktionen in `erfassen.py` und `erinnerung.py` einzeln ausprobieren. Für `speichere_eintraege` eine Dummy-Funktion, die nur `print` macht. `main.py` ruft zuerst nur die Dummy-Funktionen der anderen auf |
| C | `lade_eintraege` und `speichere_eintraege` mit den Testdaten ausprobieren, dann `zeige_eintraege` und `aendern_loeschen` |
| D | `berechne_monat` mit einer von Hand geschriebenen Liste aus zwei Dictionaries (wie in US-10) ausprobieren, mit den Einstellungen aus der Testdatei |

Bis `hilfen.py` von A da ist, darf jede Person eigene kleine Versionen von `zeit_zu_minuten` usw. in ihrer Datei haben. Danach werden sie gelöscht und die von A verwendet.

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
