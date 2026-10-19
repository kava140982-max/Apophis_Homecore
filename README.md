# KaVa Workspace Free

**Eine kostenlose, bewusst kleine Ausgabe für den eigenen Rechner.**

KaVa Workspace Free hilft dabei, einfache Notizen, Aufgaben und Verweise auf Dateien an einem Ort zu sammeln. Die Einträge werden auf Ihrem eigenen Rechner gespeichert und verschlüsselt abgelegt.

> **Für wen ist diese Anleitung?** Für Menschen, die keine IT-Ausbildung haben. Sie können die Schritte der Reihe nach abarbeiten. Wenn ein Schritt nicht klappt, bitte nicht Schlüsseldateien löschen oder Befehle aus dem Internet ausprobieren – sichern Sie die Fehlermeldung ohne persönliche Daten und fragen Sie nach Hilfe.

## Was kann die kostenlose Ausgabe?

- Notizen speichern, zum Beispiel Gesprächsnotizen oder Ideen
- Aufgaben als kurze Einträge festhalten
- Verweise auf Dateien notieren
- Einträge auf dem eigenen Gerät verschlüsselt speichern
- prüfen, ob der gespeicherte Datenbestand noch lesbar und unverändert ist
- ohne Konto und ohne Internetverbindung arbeiten

## Was ist absichtlich nicht enthalten?

Diese kostenlose Ausgabe ist ein einfacher lokaler Grundbaustein. Sie enthält keine grafische Oberfläche. Bedienung und Einrichtung erfolgen über ein Terminal-Fenster. Kalender, Kontakte, Nachrichten, KI, E-Mail, WhatsApp, Cloud-Synchronisierung, Netzwerkzugriff, mehrere Benutzer und professionelle Administration sind nicht enthalten. Es gibt keine automatische Sicherung und keinen technischen Supportvertrag.

## Was Sie brauchen

- einen Computer mit Linux, macOS oder Windows
- Python 3.10 oder neuer
- eine Internetverbindung einmalig zum Installieren der benötigten Python-Bibliothek
- einige Minuten Zeit

Python erhalten Sie auf der offiziellen Seite [python.org](https://www.python.org/downloads/). Unter Windows aktivieren Sie im Installationsprogramm die Option **„Add Python to PATH“**. Unter macOS und Linux verwenden Sie den Paketmanager Ihres Systems oder eine bereits vorhandene Python-Installation.

## Installation – Schritt für Schritt

### 1. Projektdatei herunterladen

Laden Sie auf GitHub die ZIP-Datei dieses Projekts über **Code → Download ZIP** herunter und entpacken Sie sie. Merken Sie sich den Speicherort des entpackten Projektordners. Er heißt in der Regel `Apophis_Homecore-main`.

### 2. Terminal öffnen

- **Windows:** Öffnen Sie im Startmenü „PowerShell“.
- **macOS:** Öffnen Sie „Terminal“ über Programme → Dienstprogramme.
- **Linux:** Öffnen Sie die Terminal-Anwendung Ihres Systems.

Wechseln Sie in den entpackten Ordner. Beispiel (ersetzen Sie den Pfad durch den tatsächlichen Ablageort):

```text
cd Pfad/zum/Apophis_Homecore-main
```

### 3. Virtuelle Umgebung anlegen

Eine virtuelle Umgebung hält die Bibliotheken dieses Programms getrennt von anderen Python-Programmen.

Windows:

```text
py -m venv .venv
.venv\Scripts\activate
```

macOS oder Linux:

```text
python3 -m venv .venv
source .venv/bin/activate
```

Wenn die Aktivierung geklappt hat, erscheint meist `(.venv)` am Anfang der Eingabezeile.

### 4. KaVa installieren

```text
python -m pip install -e .
```

Falls Ihr System `python` nicht kennt, versuchen Sie unter Windows `py -m pip install -e .` oder unter macOS/Linux `python3 -m pip install -e .`.

## Erste Schritte

Geben Sie die Befehle im Terminal ein, während Sie sich im Projektordner befinden und die virtuelle Umgebung aktiviert ist.

### Eine Notiz speichern

```text
kava-free add note "Einkaufsidee" "Für das Büro Papier und Stifte besorgen"
```

### Eine Aufgabe speichern

```text
kava-free add task "Angebot prüfen" "Das Angebot am Freitag noch einmal ansehen"
```

### Einen Dateiverweis speichern

```text
kava-free add file_ref "Rechnung Drucker" "Datei liegt im Ordner Dokumente/Rechnungen"
```

### Einträge anzeigen

```text
kava-free list
```

### Speicher prüfen

```text
kava-free check
```

Beim ersten Speichern legt KaVa einen verschlüsselten Datenspeicher im Ordner `data` und einen geheimen Schlüssel im Ordner `private` an. Diese Dateien sind wichtig, damit Sie Ihre gespeicherten Einträge später öffnen können.

## Bitte beachten: Schlüssel und Sicherung

- Der Ordner `private` enthält den Schlüssel. Geben Sie ihn niemals weiter und laden Sie ihn nicht ins Internet hoch.
- Ohne den Schlüssel können verschlüsselte Einträge nicht wiederhergestellt werden.
- Machen Sie eine Sicherungskopie des Ordners `data` **und** des Ordners `private` auf einem geschützten, getrennten Speicher. Bewahren Sie beide zusammen auf, aber schützen Sie den Schlüssel besonders sorgfältig.
- Löschen Sie die Schlüsseldatei nicht, solange Sie gespeicherte Einträge behalten möchten.
- Diese Ausgabe erstellt keine Sicherung automatisch.
- Verschlüsselung schützt die gespeicherte Datei. Sie ersetzt weder ein Gerätepasswort noch ein Backup und ist keine Sicherheitszertifizierung.

## Häufige Fragen

**Muss ich ein Konto anlegen?** Nein.

**Werden meine Einträge an KaVa oder an einen Cloud-Dienst gesendet?** Die hier enthaltenen Funktionen speichern lokal und enthalten keine Netzwerk-Anbindung.

**Kann ich meine Einträge in Word oder Excel öffnen?** Nicht direkt. Diese Ausgabe ist ein kleiner technischer Grundbaustein und bietet noch keinen Exportknopf.

**Was passiert, wenn ich den Schlüssel verliere?** Die verschlüsselten gespeicherten Daten können dann nicht mehr gelesen werden. Suchen Sie zuerst nach einer sicheren Sicherungskopie des Schlüssels.

**Was mache ich bei einer Fehlermeldung?** Notieren Sie den Befehl und die Fehlermeldung. Entfernen Sie vorher Namen, private Texte und andere persönliche Angaben. Teilen Sie niemals Schlüssel, Passwörter oder vertrauliche Einträge.

## Lizenz und Herkunft

KaVa und die Bestandteile dieser Ausgabe bleiben urheberrechtlich Kai Valenta zugeordnet. Die Veröffentlichung des Quelltexts macht ihn nicht automatisch zu freier Open-Source-Software und erlaubt keine kommerzielle Weitergabe oder Änderung. Die kostenlose Nutzung ist auf den privaten, nicht kommerziellen Einsatz dieser eingeschränkten Ausgabe beschränkt. Für andere Nutzungen ist eine schriftliche Freigabe erforderlich. Siehe [COPYRIGHT.md](COPYRIGHT.md).

**Kontakt:** Kava140982@gmail.com  
**Version:** 1.0.0
