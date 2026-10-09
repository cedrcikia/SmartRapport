# ⏱️ SmartRapport – Arbeitszeit-App für Temporäre (Konsole)

Gruppenprojekt im Modul **Grundlagen Programmieren**, FHNW, Herbstsemester 2026.

Mit unserer App können Temporärmitarbeitende ihre Arbeitsstunden erfassen, ihren Lohn ausrechnen lassen und am Ende einen Rapport als Textdatei erstellen. Alles läuft in der Konsole, ohne Website und ohne Zusatzprogramme.

---
## Analyse

### Problem

Viele Temporärmitarbeitende schreiben ihre Arbeitsstunden von Hand auf, auf einem Zettel oder im Handy. Am Ende des Monats ist dann oft unklar, wie viele Stunden wirklich gearbeitet wurden, ob es Überstunden gibt und wie hoch der Lohn brutto und netto ungefähr ist. Wer sich verrechnet oder den Rapport zu spät abgibt, verursacht Fehler in der Lohnabrechnung, und der Lohn kommt später.

### Szenario

Ein Temporärer arbeitet in einem Betrieb. Nach jedem Arbeitstag öffnet er SmartRapport in der Konsole und trägt Datum, Start, Ende und Pause ein. Stundenlohn, tägliche Sollzeit, Zuschlag und Abzüge gibt er einmal ein und kann sie später ändern. Am Ende des Monats lässt er sich Stunden und Lohn ausrechnen und speichert den Rapport als Textdatei. Die App erinnert ihn rechtzeitig an den Abgabetermin.

### User Roles

| Rolle | Beschreibung |
|---|---|
| **Temporärer** | Arbeitet über die Temporärfirma in einem Einsatzbetrieb. Trägt seine Stunden ein, prüft sie und will wissen, wie viel Lohn er bekommt. Bedient die App. |
| **Disponent:in** | Arbeitet bei der Temporärfirma. Legt fest, welche Zuschläge und Abzüge für alle Temporären gelten. |
| **Lohnbuchhaltung** | Zahlt den Lohn aus. Braucht einen vollständigen und nachvollziehbaren Rapport pro Monat. |

Die Konsole bedient immer der Temporäre. Die anderen beiden Rollen haben Anforderungen an die App (gleiche Sätze für alle, nachvollziehbarer Rapport), bedienen sie aber nicht selbst.

### Festlegungen für alle Stories

1. **Rapport:** Ein Rapport ist ein Kalendermonat. Ein Eintrag gehört zum Monat, der in seinem Datum steht (`05.10.2026` gehört zu `10.2026`).
2. **Arbeitszeit:** Arbeitszeit = Endzeit minus Startzeit minus Pause. Das Ende muss am selben Tag nach dem Start liegen. Nachtschichten über Mitternacht gibt es in dieser Version nicht.
3. **Überstunden:** Überstunden werden pro Tag gerechnet. Ist die Arbeitszeit eines Tages länger als die tägliche Sollzeit, ist der Rest Überstunden. Alle anderen Stunden sind Normalstunden. Auf Überstunden gibt es einen Zuschlag.
4. **Lohn:** Bruttolohn = Normalstunden × Stundenlohn + Überstunden × Stundenlohn × (1 + Zuschlag in % / 100). Jeder Abzug ist ein Prozentsatz vom Bruttolohn. Nettolohn = Bruttolohn minus alle Abzüge.
5. **Geld:** Alle Beträge sind in CHF mit zwei Nachkommastellen. Zuerst wird der Bruttolohn auf zwei Stellen gerundet, dann wird jeder Abzug einzeln von diesem Betrag berechnet und gerundet.
6. **Abgabetermin:** Der Rapport muss bis zum 25. des Monats abgegeben werden.
7. **Dateien:**
   * `stunden.txt`: eine Zeile pro Eintrag, `05.10.2026;07:30;17:00;45` (Datum, Start, Ende, Pause in Minuten). Im Code ist ein Eintrag ein Dictionary mit den Schlüsseln `datum`, `start`, `ende`, `pause_min`.
   * `einstellungen.txt`: eine Zeile pro Wert als `schluessel=wert`: `stundenlohn`, `soll_min` (tägliche Sollzeit in Minuten), `zuschlag`, `ahv`, `alv`, `nbu`. Gibt es die Datei nicht, wird sie beim Start mit Standardwerten angelegt (Stundenlohn 30.00, Sollzeit 8 Std 00 Min, Zuschlag 25, AHV 5.3, ALV 1.1, NBU 0.8).

---

## 📖 User Stories

Jede Person im Team ist für 3 User Stories zuständig.

| Person | Stories |
|---|---|
| A | US-01, US-02, US-03 |
| B | US-04, US-05, US-09 |
| C | US-06, US-07, US-08 |
| D | US-10, US-11, US-12 |

Beispielwerte: Stundenlohn CHF 32.50, Sollzeit 8 Std 00 Min pro Tag, Zuschlag 25 %, AHV 5.30 %, ALV 1.10 %, NBU 0.80 %.

### Einstellungen (Person A)

#### US-01: Stundenlohn eingeben
Als **Temporärer** möchte ich meinen Stundenlohn eingeben und ändern können, damit mein Lohn immer richtig berechnet wird.

**Akzeptanzkriterien**
* Der Lohn wird in `einstellungen.txt` gespeichert und beim Start der App geladen.
* Gegeben der Temporäre gibt `32.50` ein, wenn er bestätigt, dann erscheint `Stundenlohn gespeichert: CHF 32.50` und `einstellungen.txt` enthält `stundenlohn=32.50`.
* Gegeben `einstellungen.txt` enthält `stundenlohn=32.50`, wenn die App neu gestartet wird, dann wird CHF 32.50 verwendet.
* Gegeben die Eingabe `abc`, eine leere Eingabe, `0` oder `-5`, wenn er bestätigt, dann erscheint `Ungültiger Stundenlohn.`, nichts wird gespeichert und die App fragt erneut.

#### US-02: Tägliche Sollzeit eingeben
Als **Temporärer** möchte ich meine tägliche Sollzeit laut Vertrag eingeben, damit die App weiss, ab wann Überstunden zählen.

**Akzeptanzkriterien**
* Stunden und Minuten werden einzeln abgefragt. Stunden sind eine ganze Zahl von 1 bis 24, Minuten eine ganze Zahl von 0 bis 59.
* Die Sollzeit wird in Minuten in `einstellungen.txt` gespeichert (`soll_min`).
* Gegeben `8` Std und `0` Min, wenn er bestätigt, dann erscheint `Sollzeit gespeichert: 8 Std 00 Min pro Tag` und `einstellungen.txt` enthält `soll_min=480`.
* Gegeben Minuten `60`, Stunden `0`, Stunden `abc` oder eine leere Eingabe, dann erscheint `Ungültige Eingabe.` und die App fragt erneut.

---

#### US-03: Zuschlag und Abzüge eingeben

Als **Temporärer** möchte ich den Überstunden-Zuschlag und die Abzüge (AHV, ALV, NBU) in Prozent eingeben können, die mir von der Disponentin vorgegeben wurden, damit mein Lohn nach denselben betrieblichen Sätzen berechnet wird.

##### Mock-up-Ablauf (Konsolen-Dialog)

```
[EINSTELLUNGEN - BETRIEBLICHE SÄTZE]

Überstunden-Zuschlag in % [25]: 25
AHV-Abzug in % [5.3]: 5.3
ALV-Abzug in % [1.1]: 1.1
NBU-Abzug in % [0.8]: 0.8
```

##### Akzeptanzkriterien

* Zuschlag, AHV, ALV und NBU werden einzeln als Prozentwert abgefragt und in `einstellungen.txt` gespeichert.
* Jeder Wert ist eine Zahl von 0 bis 100 und darf Nachkommastellen haben.
* Alle Werte können später geändert werden.
* Gegeben Zuschlag `25`, AHV `5.3`, ALV `1.1` und NBU `0.8`, wenn alle bestätigt werden, dann erscheint `Sätze gespeichert` und `einstellungen.txt` enthält `zuschlag=25`, `ahv=5.3`, `alv=1.1` und `nbu=0.8`.
* Gegeben der Wert `0`, dann wird er akzeptiert.
* Gegeben der Wert `101`, `-1`, `abc` oder leer, dann erscheint `Ungültiger Prozentwert (0 bis 100).` und derselbe Wert wird erneut abgefragt.

### Stunden eintragen (US-04, US-05: Person B, US-06: Person C)

#### US-04: Arbeitstag eintragen
Als **Temporärer** möchte ich einen Arbeitstag mit Datum, Startzeit und Endzeit eintragen, damit meine Stunden festgehalten sind.

**Akzeptanzkriterien**
* Datum im Format `TT.MM.JJJJ` (z.B. `05.10.2026`), Zeiten im Format `HH:MM` (z.B. `07:30`).
* Gegeben Datum `05.10.2026`, Start `07:30` und Ende `17:00`, wenn er bestätigt, dann werden die Werte akzeptiert und die App fragt nach der Pause (US-05).
* Gegeben das Datum `31.02.2026`, `5.10.26` oder `abc`, dann erscheint `Ungültiges Datum (TT.MM.JJJJ).` und das Datum wird erneut abgefragt.
* Gegeben die Zeit `7:30`, `25:00` oder `abc`, dann erscheint `Ungültige Uhrzeit (HH:MM).` und die Zeit wird erneut abgefragt.
* Gegeben Start `17:00` und Ende `07:30`, dann erscheint `Das Ende muss nach dem Start liegen.` und das Ende wird erneut abgefragt.

#### US-05: Pause eingeben
Als **Temporärer** möchte ich meine Pause in Minuten eingeben, damit nur meine echte Arbeitszeit zählt.

**Akzeptanzkriterien**
* Die Pause wird direkt nach Start und Ende abgefragt, als ganze Zahl in Minuten.
* Danach zeigt die App die Arbeitszeit des Tages, z.B. `Arbeitszeit: 8 Std 45 Min`.
* Gegeben Start `07:30`, Ende `17:00` und Pause `45`, dann erscheint `Arbeitszeit: 8 Std 45 Min`.
* Gegeben Pause `0`, dann wird sie akzeptiert.
* Gegeben Pause `abc`, `-5`, `4.5` oder leer, dann erscheint `Ungültige Pause.` und die Pause wird erneut abgefragt.
* Gegeben Start `07:30`, Ende `17:00` (570 Min) und Pause `570` oder mehr, dann erscheint `Die Pause muss kürzer sein als die Arbeitszeit.` und die Pause wird erneut abgefragt.

#### US-06: Einträge speichern und laden
Als **Temporärer** möchte ich, dass meine Einträge automatisch gespeichert und beim nächsten Start wieder geladen werden, damit nichts verloren geht.

**Akzeptanzkriterien**
* Jeder Eintrag wird nach der Pause in `stunden.txt` gespeichert, eine Zeile pro Eintrag (siehe Festlegung 7). Beim Start werden alle gültigen Zeilen geladen.
* Gegeben Datum `05.10.2026`, Start `07:30`, Ende `17:00` und Pause `45`, dann steht `05.10.2026;07:30;17:00;45` in `stunden.txt` und es erscheint `Eintrag gespeichert`.
* Gegeben `stunden.txt` enthält 3 gültige Zeilen, wenn die App startet, dann sind 3 Einträge geladen.
* Gegeben Zeile 2 lautet `05.10.2026;07:30;abc;45`, wenn die App startet, dann erscheint `Zeile 2 übersprungen: 05.10.2026;07:30;abc;45`, die anderen Zeilen werden geladen und die App stürzt nicht ab.
* Gegeben `stunden.txt` existiert nicht, wenn die App startet, dann startet sie mit einer leeren Liste ohne Fehlermeldung.

### Einträge verwalten und Abgabetermin (US-07, US-08: Person C, US-09: Person B)

#### US-07: Einträge anzeigen
Als **Temporärer** möchte ich alle Einträge eines Monats sehen, damit ich weiss, was ich gearbeitet habe.

**Akzeptanzkriterien**
* Der Monat wird als `MM.JJJJ` eingegeben (z.B. `10.2026`).
* Die Einträge dieses Monats werden nach Datum sortiert und ab 1 nummeriert angezeigt, z.B. `1. 05.10.2026  07:30–17:00  Pause 45 Min  8 Std 45 Min`.
* Unter der Liste steht das Total der Arbeitszeit des Monats.
* Gegeben Einträge am 05.10.2026 (8 Std 45 Min), 06.10.2026 (7 Std 30 Min) und 12.11.2026, wenn `10.2026` gewählt wird, dann werden 2 Einträge als 1 und 2 angezeigt und das Total ist `16 Std 15 Min`.
* Gegeben es gibt keine Einträge in diesem Monat, dann erscheint `Keine Einträge für 10.2026.`
* Gegeben die Eingabe `13.2026`, `2026` oder `abc`, dann erscheint `Ungültiger Monat (MM.JJJJ).` und der Monat wird erneut abgefragt.

#### US-08: Eintrag ändern oder löschen
Als **Temporärer** möchte ich einen falschen Eintrag ändern oder löschen können, damit meine Stunden stimmen.

**Akzeptanzkriterien**
* Die App zeigt zuerst die Liste des gewählten Monats (wie in US-07). Der Eintrag wird über seine Nummer gewählt, danach Ändern oder Löschen.
* Beim Ändern werden Datum, Start, Ende und Pause neu abgefragt und gleich geprüft wie in US-04 und US-05.
* Nach jeder Änderung und jedem Löschen wird `stunden.txt` neu geschrieben.
* Gegeben eine Liste mit 3 Einträgen, wenn Nummer `2` gewählt und das Ende auf `16:30` geändert wird, dann zeigt die Liste das neue Ende und `stunden.txt` enthält die Änderung.
* Gegeben Nummer `2` zum Löschen, wenn die App `Wirklich löschen? (j/n)` fragt und `j` eingegeben wird, dann ist der Eintrag weg und `stunden.txt` hat eine Zeile weniger.
* Gegeben die Rückfrage wird mit `n` beantwortet, dann bleibt der Eintrag unverändert.
* Gegeben die Nummer `0`, `4` (bei 3 Einträgen) oder `abc`, dann erscheint `Ungültige Nummer.` und die Nummer wird erneut abgefragt.

#### US-09: Erinnerung an den Abgabetermin
Als **Temporärer** möchte ich beim Starten der App an den Abgabetermin erinnert werden, damit ich den Rapport nicht vergesse.

**Akzeptanzkriterien**
* Der Abgabetermin ist der 25. jedes Monats. Die Erinnerung erscheint beim Start vom 22. bis und mit 25., und nur wenn die Datei `rapport_MM_JJJJ.txt` für diesen Monat noch nicht existiert.
* Gegeben das heutige Datum ist `22.10.2026` und `rapport_10_2026.txt` existiert nicht, dann erscheint `Rapport Oktober bis 25.10.2026 abgeben – noch 3 Tage`.
* Gegeben das heutige Datum ist `25.10.2026`, dann lautet der Hinweis `... – noch 0 Tage`.
* Gegeben das heutige Datum ist `21.10.2026` oder `26.10.2026`, dann erscheint keine Erinnerung.
* Gegeben das heutige Datum ist `22.10.2026` und `rapport_10_2026.txt` existiert, dann erscheint keine Erinnerung.

### Berechnung und Rapport (Person D)

#### US-10: Überstunden ausrechnen
Als **Temporärer** möchte ich, dass die App meine Überstunden selbst ausrechnet, damit ich das nicht von Hand machen muss.

**Akzeptanzkriterien**
* Für jeden Eintrag des gewählten Monats werden Normalstunden und Überstunden berechnet (Regel siehe Festlegung 3). Danach wird über den Monat summiert.

| Sollzeit | Arbeitszeit des Tages | Normalstunden | Überstunden |
|---|---|---|---|
| 8:00 | 10:00 | 8:00 | 2:00 |
| 8:00 | 8:00 | 8:00 | 0:00 |
| 8:00 | 7:30 | 7:30 | 0:00 |

* Gegeben Sollzeit 8 Std 00 Min und zwei Einträge mit 8 Std 45 Min und 7 Std 30 Min, wenn der Monat berechnet wird, dann sind die Normalstunden `15 Std 30 Min` und die Überstunden `0 Std 45 Min`.
* Gegeben ein Monat ohne Einträge, dann sind beide Werte `0 Std 00 Min`.

#### US-11: Übersicht anzeigen
Als **Temporärer** möchte ich eine Übersicht über meine Stunden und meinen Lohn sehen, damit ich weiss, was ich ungefähr verdiene.

**Akzeptanzkriterien**
* Die Übersicht wird für einen gewählten Monat angezeigt: Normalstunden, Überstunden, Bruttolohn, jeder Abzug einzeln und Nettolohn (Regeln siehe Festlegung 4 und 5).
* Gegeben Stundenlohn 32.50, Zuschlag 25 %, AHV 5.30 %, ALV 1.10 %, NBU 0.80 % und die Stunden aus US-10 (15 Std 30 Min normal, 0 Std 45 Min Überstunden), dann erscheint:

```
Normalstunden:     15 Std 30 Min
Überstunden:        0 Std 45 Min
Brutto:            CHF 534.22
AHV (5.30 %):      -CHF 28.31
ALV (1.10 %):      -CHF 5.88
NBU (0.80 %):      -CHF 4.27
Netto:             CHF 495.76
```

* Gegeben alle Abzüge sind 0 %, dann ist der Nettolohn gleich dem Bruttolohn.
* Gegeben der Monat hat keine Einträge, dann erscheint `Keine Einträge für 10.2026.` und es wird nichts berechnet.

#### US-12: Rapport als Datei speichern
Als **Lohnbuchhaltung** möchte ich vom Temporären einen Rapport als Textdatei erhalten, damit ich seine Stunden prüfen und mit der Lohnabrechnung vergleichen kann.

**Akzeptanzkriterien**
* Der Temporäre wählt den Monat, die App speichert den Rapport als `rapport_<MM>_<JJJJ>.txt`, z.B. `rapport_10_2026.txt`.
* Die Datei enthält den Monat, den Abgabetermin (`Abgabetermin: 25.10.2026`), alle Einträge (wie in US-07) und die Lohnübersicht (wie in US-11). Die Beträge sind identisch mit denen der Übersicht.
* Gegeben der Monat `10.2026` mit Einträgen, wenn der Rapport gespeichert wird, dann erscheint `Rapport gespeichert als rapport_10_2026.txt` und die Datei existiert.
* Gegeben `rapport_10_2026.txt` existiert schon, dann fragt die App `Datei existiert bereits. Überschreiben? (j/n)`. Bei `j` wird sie überschrieben, bei `n` bleibt sie unverändert.
* Gegeben der Monat hat keine Einträge, dann erscheint `Keine Einträge – Rapport nicht erstellt.` und es wird keine Datei angelegt.

---

## 👥 Aufgabenverteilung

### Überblick

| Person | Schwierigkeit | Stories | Eigene Dateien |
|---|---|---|---|
| **A** | sehr einfach | US-01 Stundenlohn, US-02 Sollzeit, US-03 Zuschlag und Abzüge | `einstellungen.py`, `hilfen.py` |
| **B** | mittelleicht | US-04 Arbeitstag, US-05 Pause, US-09 Erinnerung | `erfassen.py`, `erinnerung.py`, `main.py` |
| **C** | mittelschwer | US-06 Speichern und Laden, US-07 Einträge anzeigen, US-08 Ändern und Löschen | `speicher.py`, `verwaltung.py` |
| **D** | schwer (die 3 schwierigsten) | US-10 Überstunden, US-11 Übersicht, US-12 Rapport-Datei | `berechnung.py`, `rapport.py` |

**Warum so:**
* A schreibt dreimal dasselbe Muster (fragen, prüfen, speichern). Dazu kommt `hilfen.py`, eine Sammlung kleiner Funktionen, die alle brauchen. Das ist kurz, aber wichtig.
* B prüft Eingaben (Datum, Uhrzeit, Pause) und baut das Hauptmenü.
* C arbeitet mit Listen und Dictionaries: Dateien lesen und schreiben, sortieren, nummerieren, ändern, löschen.
* D rechnet: Überstunden pro Tag, Lohn, Abzüge, Rundung, und schreibt die Rapport-Datei.

---

### Regeln, damit ihr parallel arbeiten könnt

1. **Jede Person bearbeitet nur ihre eigenen Dateien.** Nur so gibt es keine Konflikte in Git. `main.py` gehört B. Wenn ihr etwas im Menü braucht, sagt es B.
2. **Die Funktionsnamen unten sind fix.** Sie sind der Vertrag zwischen euch. Namen, Parameter und Rückgabewerte ändert nur ihr gemeinsam im Team.
3. **Niemand wartet auf andere.** Jede Person testet zuerst mit Testdaten und kleinen Dummy-Funktionen (siehe unten). Erst wenn die anderen Teile fertig sind, setzt ihr alles zusammen.
4. **Regelmässig committen, mit eigenem Namen.** Die Dozierenden prüfen die Beiträge über die Commits.
5. **Kurz erklären können, was die Funktion tut.** Schreibt bei jeder Funktion einen Kommentar in eigenen Worten.

---

### Gemeinsame Datenformen

**Ein Eintrag** (Dictionary), z.B.:

```
{"datum": "05.10.2026", "start": "07:30", "ende": "17:00", "pause_min": 45}
```

`pause_min` ist eine Zahl, alles andere Text.

**Einstellungen** (Dictionary), z.B.:

```
{"stundenlohn": 32.5, "soll_min": 480, "zuschlag": 25.0, "ahv": 5.3, "alv": 1.1, "nbu": 0.8}
```

**Monat** ist immer ein Text im Format `"10.2026"`.

**Ergebnis der Berechnung** (Dictionary, das D liefert):

```
{"normal_min": 930, "ueber_min": 45, "brutto": 534.22,
 "abzuege": {"AHV": 28.31, "ALV": 5.88, "NBU": 4.27}, "netto": 495.76}
```

---

### Schnittstellen (die Funktionen, die ihr einander anbietet)

#### `hilfen.py` (Person A)

| Funktion | Gibt zurück | Zweck |
|---|---|---|
| `zeit_zu_minuten(text)` | Zahl | `"07:30"` wird zu `450` |
| `minuten_zu_text(minuten)` | Text | `525` wird zu `"8 Std 45 Min"` |
| `ist_gueltiges_datum(text)` | `True`/`False` | prüft `TT.MM.JJJJ` und ob das Datum existiert |
| `ist_gueltige_uhrzeit(text)` | `True`/`False` | prüft `HH:MM` |
| `ist_gueltiger_monat(text)` | `True`/`False` | prüft `MM.JJJJ` |
| `frage_monat()` | Text | fragt den Monat ab, bis er gültig ist |
| `frage_ja_nein(frage)` | `True`/`False` | fragt `j/n` ab, bis die Eingabe stimmt |
| `arbeitszeit_minuten(eintrag)` | Zahl | Ende minus Start minus Pause |
| `rapport_dateiname(monat)` | Text | `"10.2026"` wird zu `"rapport_10_2026.txt"` |

#### `einstellungen.py` (Person A)

| Funktion | Zweck |
|---|---|
| `lade_einstellungen()` | liest `einstellungen.txt`, legt sie mit Standardwerten an, falls sie fehlt. Gibt das Einstellungs-Dictionary zurück |
| `speichere_einstellungen(einstellungen)` | schreibt `einstellungen.txt` |
| `stundenlohn_eingeben(einstellungen)` | US-01 |
| `sollzeit_eingeben(einstellungen)` | US-02 |
| `saetze_eingeben(einstellungen)` | US-03 |

#### `erfassen.py` (Person B)

| Funktion | Zweck |
|---|---|
| `frage_datum()` | fragt ein Datum ab, bis es gültig ist. Gibt Text zurück |
| `frage_uhrzeit(text)` | fragt eine Uhrzeit mit dem Fragetext ab. Gibt Text zurück |
| `frage_pause(max_min)` | fragt die Pause ab, sie muss kürzer als `max_min` sein. Gibt eine Zahl zurück |
| `arbeitstag_eintragen(eintraege)` | US-04 und US-05: fragt alles ab, hängt den Eintrag an die Liste an und speichert (ruft `speichere_eintraege` auf) |

#### `erinnerung.py` (Person B)

| Funktion | Zweck |
|---|---|
| `pruefe_erinnerung(heute)` | US-09: zeigt den Hinweis oder nichts. `heute` ist ein `date`-Objekt. So lässt sich jeder Tag testen |

#### `speicher.py` (Person C)

| Funktion | Zweck |
|---|---|
| `lade_eintraege()` | US-06: liest `stunden.txt`, überspringt kaputte Zeilen mit Meldung. Gibt die Liste der Einträge zurück |
| `speichere_eintraege(eintraege)` | schreibt die ganze Liste in `stunden.txt` |

#### `verwaltung.py` (Person C)

| Funktion | Zweck |
|---|---|
| `eintraege_des_monats(eintraege, monat)` | Einträge dieses Monats, nach Datum sortiert. D braucht diese Funktion auch |
| `zeige_eintraege(eintraege)` | US-07: fragt den Monat ab und zeigt die nummerierte Liste mit Total |
| `aendern_loeschen(eintraege)` | US-08: Liste zeigen, Nummer wählen, ändern oder löschen, speichern |

#### `berechnung.py` (Person D)

| Funktion | Zweck |
|---|---|
| `berechne_monat(monats_eintraege, einstellungen)` | US-10 und Lohn: gibt das Ergebnis-Dictionary zurück |
| `zeige_uebersicht(eintraege, einstellungen)` | US-11: fragt den Monat ab und zeigt die Übersicht |

#### `rapport.py` (Person D)

| Funktion | Zweck |
|---|---|
| `rapport_speichern(eintraege, einstellungen)` | US-12: fragt den Monat ab, fragt bei bestehender Datei nach und schreibt `rapport_MM_JJJJ.txt` |

#### `main.py` (Person B)

Lädt Einstellungen und Einträge, ruft `pruefe_erinnerung` auf und zeigt das Hauptmenü. Jeder Menüpunkt ruft genau eine der obigen Funktionen auf.

---

### Wie jede Person ohne die anderen anfangen kann

**Testdaten** (legt sie in eure Arbeitsordner, alle haben dieselben):

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
nbu=0.8
```

Mit diesen Daten ist das erwartete Ergebnis für den Monat `10.2026` bekannt: 15 Std 30 Min normal, 0 Std 45 Min Überstunden, Brutto CHF 534.22, Netto CHF 495.76. Das sind die Testfälle für D.

**Was jede Person am Anfang tut:**

| Person | Erster Schritt, ohne auf andere zu warten |
|---|---|
| A | `hilfen.py` zuerst, weil alle sie brauchen. Danach `einstellungen.py` |
| B | Die Funktionen in `erfassen.py` und `erinnerung.py` einzeln ausprobieren. Für `speichere_eintraege` eine leere Dummy-Funktion, die nur `print` macht. `main.py` ruft zuerst nur die Dummy-Funktionen der anderen auf |
| C | `lade_eintraege` und `speichere_eintraege` mit den Testdaten ausprobieren, dann `zeige_eintraege` und `aendern_loeschen` |
| D | `berechne_monat` mit einer von Hand geschriebenen Liste aus zwei Dictionaries (wie in US-10) ausprobieren, mit den Einstellungen aus der Testdatei |

Bis `hilfen.py` von A da ist, könnt ihr eure eigenen kleinen Versionen von `zeit_zu_minuten` usw. in eurer Datei haben. Danach löscht ihr sie und nehmt die von A.

---

### Reihenfolge (Vorschlag)

| Wann | Ziel |
|---|---|
| bis So 11.10. | User Stories fertig und auf Moodle abgegeben (Frist: 12.10., 00:00) |
| bis So 18.10. | Repository mit allen leeren Dateien und den Funktionsnamen, Testdaten im Repo, A liefert `hilfen.py` |
| bis So 1.11. | Jede Person: ihre Stories laufen einzeln mit Testdaten |
| bis So 15.11. | Zusammensetzen in `main.py`, gemeinsam alle Akzeptanzkriterien durchspielen |
| bis So 29.11. | Fehler beheben, README fertig (Anforderungen, Implementation, Beiträge), Folien |
| bis So 6.12., 23:55 | Abgabe: PDF der Folien mit Link zum **öffentlichen** Repo |

Schaut das mit den Meilensteinen im Semesterprogramm von Felix nach. Wenn es dort frühere Termine gibt, gelten diese.

---

### Wenn jemand zu langsam oder zu schnell ist

* **A fertig:** übernimmt Tests für alle (die Beispiele aus den Akzeptanzkriterien nachspielen), die README-Abschnitte Anforderungen und Libraries und hilft D.
* **D hängt:** A oder B übernimmt US-11 (Übersicht). Das ist nur Anzeige, wenn `berechne_monat` schon das Ergebnis liefert. Meldet das früh im Team, vor allem, weil die Beiträge in Git sichtbar sein müssen.
