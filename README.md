# ⏱️ SmartRappor – Arbeitszeit-App für Temporäre (Konsole)

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
| A (Einstellungen) | US-01, US-02, US-03 |
| B (Stunden erfassen) | US-04, US-05, US-06 |
| C (Verwalten und Termin) | US-07, US-08, US-09 |
| D (Berechnung und Rapport) | US-10, US-11, US-12 |

Beispielwerte: Stundenlohn CHF 32.50, Sollzeit 8 Std 00 Min pro Tag, Zuschlag 25 %, AHV 5.30 %, ALV 1.10 %, NBU 0.80 %.

### Person A – Einstellungen

#### US-01: Stundenlohn eingeben
Als **Temporärer** möchte ich meinen Stundenlohn eingeben und ändern können, damit mein Lohn immer richtig berechnet wird.

**Akzeptanzkriterien**
* Der Lohn wird in `einstellungen.txt` gespeichert und beim Start der App geladen.
* Gegeben der Temporäre gibt `32.50` ein, wenn er bestätigt, dann erscheint ` Stundenlohn gespeichert: CHF 32.50` und `einstellungen.txt` enthält `stundenlohn=32.50`.
* Gegeben `einstellungen.txt` enthält `stundenlohn=32.50`, wenn die App neu gestartet wird, dann wird CHF 32.50 verwendet.
* Gegeben die Eingabe `abc`, eine leere Eingabe, `0` oder `-5`, wenn er bestätigt, dann erscheint `Ungültiger Stundenlohn.`, nichts wird gespeichert und die App fragt erneut.

#### US-02: Tägliche Sollzeit eingeben
Als **Temporärer** möchte ich meine tägliche Sollzeit laut Vertrag eingeben, damit die App weiss, ab wann Überstunden zählen.

**Akzeptanzkriterien**
* Stunden und Minuten werden einzeln abgefragt. Stunden sind eine ganze Zahl von 1 bis 24, Minuten eine ganze Zahl von 0 bis 59.
* Die Sollzeit wird in Minuten in `einstellungen.txt` gespeichert (`soll_min`).
* Gegeben `8` Std und `0` Min, wenn er bestätigt, dann erscheint ` Sollzeit gespeichert: 8 Std 00 Min pro Tag` und `einstellungen.txt` enthält `soll_min=480`.
* Gegeben Minuten `60`, Stunden `0`, Stunden `abc` oder eine leere Eingabe, dann erscheint `Ungültige Eingabe.` und die App fragt erneut.

Hier ist die User Story **US-03** im Stil einer **Mock-up-Language** (Dialog-Skript für den Konsolen-Ablauf, wie er in der App stattfinden soll):

---

#### US-03: Zuschlag und Abzüge eingeben

Als **Temporärer** möchte ich den Überstunden-Zuschlag und die Abzüge (AHV, ALV, NBU) in Prozent eingeben können, die mir von der Disponentin vorgegeben wurden, damit mein Lohn nach denselben betrieblichen Sätzen berechnet wird.

##### Mock-up-Ablauf (Konsolen-Dialog)

[EINSTELLUNGEN - BETRIEBLICHE SÄTZE]

Stundenlohn [CHF 32.50]: 
Tägliche Sollzeit [8 Std 00 Min]: 

Überstunden-Zuschlag in % [25]: 25
AHV-Abzug in % [5.3]: 5.3
ALV-Abzug in % [1.1]: 1.1
NBU-Abzug in % [0.8]: 0.8

##### Akzeptanzkriterien

* Zuschlag, AHV, ALV und NBU werden einzeln als Prozentwert abgefragt und in `einstellungen.txt` gespeichert.
* Jeder Wert ist eine Zahl von 0 bis 100 und darf Nachkommastellen haben.
* Alle Werte können später geändert werden.
* Gegeben Zuschlag `25`, AHV `5.3`, ALV `1.1` und NBU `0.8`, wenn alle bestätigt werden, dann erscheint ` Sätze gespeichert` und `einstellungen.txt` enthält `zuschlag=25`, `ahv=5.3`, `alv=1.1` und `nbu=0.8`.
* Gegeben der Wert `0`, dann wird er akzeptiert.
* Gegeben der Wert `101`, `-1`, `abc` oder leer, dann erscheint `Ungültiger Prozentwert (0 bis 100).` und derselbe Wert wird erneut abgefragt.

### Person B – Stunden eintragen

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
* Gegeben Datum `05.10.2026`, Start `07:30`, Ende `17:00` und Pause `45`, dann steht `05.10.2026;07:30;17:00;45` in `stunden.txt` und es erscheint ` Eintrag gespeichert`.
* Gegeben `stunden.txt` enthält 3 gültige Zeilen, wenn die App startet, dann sind 3 Einträge geladen.
* Gegeben Zeile 2 lautet `05.10.2026;07:30;abc;45`, wenn die App startet, dann erscheint `Zeile 2 übersprungen: 05.10.2026;07:30;abc;45`, die anderen Zeilen werden geladen und die App stürzt nicht ab.
* Gegeben `stunden.txt` existiert nicht, wenn die App startet, dann startet sie mit einer leeren Liste ohne Fehlermeldung.

### Person C – Einträge verwalten und Abgabetermin

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

### Person D – Berechnung und Rapport

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
* Gegeben der Monat `10.2026` mit Einträgen, wenn der Rapport gespeichert wird, dann erscheint ` Rapport gespeichert als rapport_10_2026.txt` und die Datei existiert.
* Gegeben `rapport_10_2026.txt` existiert schon, dann fragt die App `Datei existiert bereits. Überschreiben? (j/n)`. Bei `j` wird sie überschrieben, bei `n` bleibt sie unverändert.
* Gegeben der Monat hat keine Einträge, dann erscheint `Keine Einträge – Rapport nicht erstellt.` und es wird keine Datei angelegt.
