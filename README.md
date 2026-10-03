# ⏱️ SmartRappor – Arbeitszeit-App für Temporäre (Konsole)

Gruppenprojekt im Modul **Grundlagen Programmieren**, FHNW, Herbstsemester 2026.

Mit unserer App können Temporärmitarbeitende ihre Arbeitsstunden erfassen, ihren Lohn ausrechnen lassen und am Ende einen Rapport als Textdatei erstellen. Alles läuft in der Konsole, ohne Website und ohne Zusatzprogramme.

---

## 📝 Analyse

### Problem

Viele Temporäre schreiben ihre Stunden von Hand auf, auf einem Zettel oder im Handy. Am Ende vom Monat weiss man dann oft nicht mehr genau:

- Wie viele Stunden habe ich wirklich gearbeitet?
- Habe ich Überstunden gemacht und bekomme ich dafür einen Zuschlag?
- Wie viel Lohn bekomme ich ungefähr, brutto und netto?
- Bis wann muss ich meinen Rapport abgeben?

Wenn man sich verrechnet oder den Rapport zu spät abgibt, gibt es Fehler bei der Lohnabrechnung oder der Lohn kommt später.

### Szenario

Ein Temporärer arbeitet in einem Betrieb. Nach jedem Arbeitstag öffnet er unsere App und trägt ein, wann er angefangen und aufgehört hat und wie lange er Pause gemacht hat.

Seinen Stundenlohn, seine Wochenstunden laut Vertrag, die Zuschläge und die Abzüge gibt er einmal am Anfang ein. Er kann sie später jederzeit ändern.

Der Lohn wird immer am **letzten Donnerstag im Monat** ausbezahlt. Der Rapport muss spätestens am **Freitag davor** abgegeben werden. Die App erinnert ihn 3 Tage vorher daran. Danach kann er den Rapport als Textdatei speichern und abgeben.

---

## 👤 User Stories

Jede Person im Team ist für 3 User Stories zuständig.

### Person A – Einstellungen

**1. Stundenlohn eingeben**
Als Temporärer möchte ich meinen Stundenlohn eingeben und ändern können, damit mein Lohn immer richtig berechnet wird.

- Der Lohn muss eine positive Zahl sein, z.B. `32.50`
- Bei Buchstaben, leerer Eingabe oder Minuszahlen kommt eine Fehlermeldung und man muss nochmals eingeben
- Der Lohn wird in `einstellungen.txt` gespeichert und beim nächsten Start wieder geladen

**2. Wochenstunden und Überstunden-Grenze eingeben**
Als Temporärer möchte ich eingeben, wie viele Stunden pro Woche ich laut Vertrag arbeite und ab wann Überstunden einen Zuschlag geben, damit meine Überstunden extra angezeigt und richtig bezahlt werden.

- Man gibt die Zeit in Stunden und Minuten ein, z.B. `42 Std 00 Min` (nicht 42.0)
- Dazu gibt man ein, ab wie vielen Stunden pro Woche es einen Zuschlag gibt, z.B. ab `45 Std 00 Min`
- Alles zwischen 42 und 45 Stunden sind dann Überstunden ohne Zuschlag, alles über 45 Stunden mit Zuschlag
- Die Minuten müssen zwischen 0 und 59 liegen, und die Zuschlags-Grenze darf nicht kleiner sein als die Wochenstunden
- Wird in `einstellungen.txt` gespeichert

**3. Zuschläge und Abzüge eingeben**
Als Temporärer möchte ich die Prozente für Zuschläge (Überstunden, Nacht, Sonntag) und Abzüge (z.B. AHV, ALV, NBU) selbst eingeben, damit Brutto- und Nettolohn stimmen.

- Jeder Wert muss zwischen 0 und 100 % sein
- Man kann alles später ändern
- Wird in `einstellungen.txt` gespeichert

### Person B – Stunden eintragen

**4. Arbeitstag eintragen**
Als Temporärer möchte ich einen Arbeitstag mit Datum, Startzeit und Endzeit eintragen, damit meine Stunden gespeichert sind.

- Das Datum muss so aussehen: `TT.MM.JJJJ`, z.B. `05.10.2026`
- Die Uhrzeit muss so aussehen: `HH:MM`, z.B. `07:30`
- Wenn die Endzeit vor der Startzeit liegt, wird das als Nachtschicht über Mitternacht erkannt
- Wenn es für dieses Datum schon einen Eintrag gibt, kommt eine Warnung

**5. Pause eingeben**
Als Temporärer möchte ich meine Pause in Stunden und Minuten eingeben, damit nur die echte Arbeitszeit zählt.

- Stunden und Minuten werden einzeln abgefragt (Minuten 0 bis 59)
- Die Pause darf nicht länger sein als die Arbeitszeit
- Danach zeigt die App an, wie viel man heute und diese Woche gearbeitet hat, z.B.
  `Heute: 8 Std 45 Min – Woche 41: 38 Std 15 Min von 42 Std 00 Min`

**6. Einträge speichern und laden**
Als Temporärer möchte ich, dass meine Einträge automatisch gespeichert werden, damit beim nächsten Start nichts weg ist.

- Alle Einträge werden in `stunden.txt` gespeichert, eine Zeile pro Tag, z.B. `05.10.2026;07:30;17:00;45`
- Beim Start werden die Einträge geladen
- Wenn eine Zeile kaputt ist, wird sie übersprungen und die App zeigt eine Meldung, aber sie stürzt nicht ab

### Person C – Einträge verwalten und Abgabetermin

**7. Einträge anzeigen**
Als Temporärer möchte ich alle Einträge von einem Rapport nach Wochen sortiert sehen, damit ich weiss, wie viel ich pro Woche gearbeitet habe.

- Man gibt den Monat ein, z.B. `10.2026`, und die App zeigt, welcher Zeitraum dazugehört
- Die Einträge werden nach Datum sortiert, nummeriert und pro Woche (Montag bis Sonntag) angezeigt
- Unter jeder Woche steht das Total und die Überstunden
- Wenn es keine Einträge gibt, kommt eine Meldung

**8. Eintrag ändern oder löschen**
Als Temporärer möchte ich einen falschen Eintrag ändern oder löschen können, damit meine Stunden stimmen.

- Man wählt den Eintrag über seine Nummer aus, und die Nummer muss existieren
- Beim Ändern werden die neuen Werte gleich geprüft wie beim Eintragen
- Vor dem Löschen fragt die App nochmals nach (`j/n`)
- Danach wird `stunden.txt` aktualisiert

**9. Erinnerung an den Abgabetermin**
Als Temporärer möchte ich beim Starten der App an den Abgabetermin erinnert werden, damit ich den Rapport nicht vergesse und meinen Lohn pünktlich bekomme.

- Die App rechnet selbst aus, wann der Zahltag ist (letzter Donnerstag im Monat) und wann der Abgabetermin ist (der Freitag davor)
- Wenn der Abgabetermin auf einen Feiertag fällt, gilt der Arbeitstag davor. Die Feiertage stehen in `feiertage.txt`
- 3 Tage vor dem Termin kommt beim Start ein Hinweis, z.B.
  `⚠️ Rapport Oktober bis Freitag, 23.10.2026 abgeben – noch 3 Tage (Zahltag: Do, 29.10.2026)`
- Der Hinweis kommt nur, wenn der Rapport für diesen Monat noch nicht erstellt wurde

### Person D – Berechnung und Rapport

**10. Überstunden ausrechnen**
Als Temporärer möchte ich, dass die App meine Überstunden pro Woche selbst ausrechnet, damit ich das nicht von Hand machen muss.

- Pro Woche (Montag bis Sonntag) werden alle Stunden zusammengezählt
- Beispiel mit 42 Std laut Vertrag und Zuschlag ab 45 Std: Wer in einer Woche 47 Std 30 Min arbeitet, hat 42 Std normal, 3 Std Überstunden ohne Zuschlag und 2 Std 30 Min mit Zuschlag
- Nachtstunden (23 bis 6 Uhr) und Sonntagsstunden werden auch erkannt
- Ein Rapport geht immer über ganze Wochen, bis zum Sonntag vor dem Abgabetermin

**11. Übersicht anzeigen**
Als Temporärer möchte ich eine Übersicht über meine Stunden und meinen Lohn sehen, damit ich weiss, was ich verdient habe.

- Pro Woche: Total, Überstunden ohne und mit Zuschlag, alles in Stunden und Minuten
- Darunter: Bruttolohn, alle Abzüge einzeln und Nettolohn in CHF

**12. Rapport als Datei speichern**
Als Temporärer möchte ich meinen Rapport als Textdatei speichern, damit ich ihn abgeben und mit meiner Lohnabrechnung vergleichen kann.

- Die Datei heisst z.B. `rapport_10_2026.txt`
- Darin stehen Zeitraum, Abgabetermin, Zahltag, alle Tage nach Wochen sortiert und die Lohnübersicht
- Wenn es die Datei schon gibt, fragt die App, ob sie überschrieben werden soll

---

