# SensorLink: einmalige Einrichtung pro Windows-Rechner

Version 2, Stand 26.11.2026. Paket passend zum zuletzt bestaetigten Repository-Stand
74524cc4 (die Generatoren entsprechen ea245e14). Die Firmware wird nicht geaendert.

## Paket einspielen

Das ZIP ist ein Ergaenzungspaket, kein vollstaendiges Repository.
Im Explorer das ZIP entpacken. Den INHALT des Ordners SensorLink_Windows_Setup
in den bestehenden Projekt-Hauptordner kopieren (neben platformio.ini).
Drei bestehende Dateien werden ersetzt:

- run_setup.py
- mLRS/Common/mavlink/fmav_generate_c_library.py
- mLRS/Common/dronecan/dronecan_generate_c_library.py

Vorher `git status --short` pruefen. Bei eigenen Aenderungen an diesen drei
Dateien erst sichern/zusammenfuehren; nicht unbesehen ersetzen. Ein sauberer
Git-Stand bewahrt die bisherigen Versionen in der Historie.
Neue Dateien: setup_windows.ps1, setup_windows.cmd, requirements-setup.txt
tools/setup_cleanup.py und diese Anleitung. Vorhandene Verzeichnisse zusammenfuehren, nicht loeschen.

## Ein Befehl

PlatformIO IDE muss auf dem Rechner eingerichtet sein; Git muss im PATH liegen.
Im Projektordner in PowerShell:

```powershell
.\setup_windows.cmd
```

Der CMD-Starter erlaubt das lokale PowerShell-Skript nur fuer den gestarteten
Prozess; er aendert keine dauerhafte Windows-Ausfuehrungsrichtlinie. Eine
administrativ vorgegebene Richtlinie wird damit nicht aufgehoben.
Alternativ, wenn lokale Skripte bereits erlaubt sind:

```powershell
.\setup_windows.ps1
```

Abweichendes PlatformIO-Python kann explizit angegeben werden:

```powershell
.\setup_windows.cmd -PythonPath "D:\PlatformIO\penv\Scripts\python.exe"
```

## Was eingerichtet wird

1. Plattform-Python unter %USERPROFILE%\.platformio\penv\Scripts\python.exe
   auswaehlen. Anaconda und python-Aliase im PATH entscheiden nicht mehr.
2. Gepinnte direkte Build-Abhaengigkeiten installieren: empy 3.3.4, dronecan
   1.0.27, pexpect 4.9.0, lxml 6.1.3 und intelhex 2.3.0.
3. Importe pruefen.
4. Git-Submodule auf die im Repository festgelegten Commits initialisieren.
5. STM32-Treiber kopieren; MAVLink und DroneCAN generieren.
6. Die wesentlichen generierten Header/Quellen auf Vorhandensein und Inhalt pruefen.

Die beiden Generatoren erneuern ihre jeweiligen out-Verzeichnisse wie schon
im bisherigen Setup. Dort keine eigenen Quellcodeaenderungen pflegen.
Das Skript bricht bei Fehlern mit Fehlercode 1 ab. Erfolg endet mit SETUP OK
und FERTIG. Es gibt keine Enter-Abfrage beim automatischen Aufruf.
Internet wird fuer fehlende Pakete und Submodule benoetigt. Es wird kein
Quellstand gepullt, keine Firmware geflasht und nichts automatisch committet.

Die Paketliste betrifft die Build-Tools. Tkinter, pyserial und bleak fuer
optionale PC-Terminals/BLE-Monitore gehoeren nicht zu diesem Firmware-Setup.
Die komplette PlatformIO-Umgebung und alle transitiven Python-Abhaengigkeiten
sind damit nicht eingefroren; die Plattformversionen stehen in platformio.ini.

## Danach bauen

VS Code > PlatformIO > Project Tasks > rx-heltec-v43-868 > General > Build.
Alternativ im Projektordner:

```powershell
& "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe" run -e rx-heltec-v43-868
```

Die gleiche Einrichtung gilt auch fuer die anderen TTGO-/Heltec-Ziele.
Nach einem frischen Klon oder einer reparierten Python-Umgebung erneut laufen
lassen. Nicht vor jedem Build erforderlich.

## Ins eigene Git-Repository aufnehmen

```powershell
git diff --stat
git add -- setup_windows.ps1 setup_windows.cmd requirements-setup.txt run_setup.py tools/setup_cleanup.py mLRS/Common/mavlink/fmav_generate_c_library.py mLRS/Common/dronecan/dronecan_generate_c_library.py docs/Windows_Setup_DE.md
git diff --cached --stat
git commit -m "Add one-command Windows setup with consistent Python interpreter"
git push origin main
```

Auf den anderen Rechnern mit sauberem Arbeitsstand:

```powershell
git pull --ff-only
.\setup_windows.cmd
```

Bei lokalen Aenderungen erst `git status` pruefen und diese sichern.
Kein Force-Push, kein Kopieren von .platformio oder .pio zwischen Rechnern.

## Pruefung dieses Pakets

- Fuenf automatisierte Tests: derselbe Interpreter fuer alle Unterprozesse,
  Fehlerabbruch, fehlende/leere Header und Argumente mit Leerzeichen.
- Beide echten Generatoren erfolgreich in einem Pfad mit Leerzeichen ausgefuehrt.
- Python-Abhaengigkeiten in einer frischen isolierten Umgebung installiert.
- Tests erfolgten unter Linux. Der Windows-PowerShell-Starter und ein kompletter
  PlatformIO-Firmwarebuild wurden fuer dieses Paket hier nicht ausgefuehrt.
- Es wurde nichts auf GitHub gepusht. Erst der obige Commit/Push verteilt die
  neue Einrichtung an die anderen Rechner.

## Korrekturen in Version 2

- Importpruefung ohne verschachtelte Anfuehrungszeichen (Windows PowerShell 5.1).
- Gemeinsame Bereinigung fuer MAVLink und DroneCAN in tools/setup_cleanup.py.
- Schreibschutz wird bei einem passenden Berechtigungsfehler aufgehoben.
- Kurze Wiederholungen bei voruebergehendem Zugriffskonflikt.
- Bleibt eine Datei gesperrt, Abbruch mit Originalfehler und betroffenem Pfad.
- Nur die beiden generierten out-Ordner werden erneuert; Backupordner bleiben.

Erneut den gesamten Paketinhalt in den Projekt-Hauptordner kopieren,
Ordner zusammenfuehren und Paketdateien ersetzen. Insbesondere tools/setup_cleanup.py
muss vorhanden sein. Danach .\setup_windows.cmd starten. Zweimal hintereinander
starten, um die erneute Bereinigung auf deinem Windows-Rechner zu pruefen.
Die gesperrten Dateien werden nicht uebergangen und fremde Prozesse nicht beendet.

Version-2-Test: fuenf weitere Bereinigungstests bestanden (wiederholter Lauf,
Backup-Erhalt, erlaubte Pfade, Schreibschutzbehandlung, Sperrfehler und Dateipfad).
Beide echten Generatoren zweimal hintereinander im Pfad mit Leerzeichen
erfolgreich ausgefuehrt. Windows-Sperren wurden simuliert; Windows-Hardwaretest offen.
