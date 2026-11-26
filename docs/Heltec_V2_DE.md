# Heltec WiFi LoRa 32 V2 – SensorLink, 868 MHz

Eigenständige Ziele für **Heltec WiFi LoRa 32 V2 mit ESP32 und SX1276** in der 868-MHz-Ausführung. Nicht für V3/V4. Bestehende TTGO- und V4.3-Ziele bleiben erhalten. Grundlage: SensorLink ea245e14 / 74524cc4 (Handbuch).

## Installation

1. ZIP nach Downloads entpacken. Den tatsächlichen Pfad zur `install_heltec_v2.py` beachten (Windows kann einen zusätzlichen gleichnamigen Unterordner erzeugen).
2. VS Code mit dem vorhandenen mLRS-SensorLink-Ordner öffnen. PowerShell-Terminal im Projektordner:

```powershell
& "$env:USERPROFILE\.platformio\penv\Scripts\python.exe" "$env:USERPROFILE\Downloads\Heltec_V2_868\install_heltec_v2.py"
```

Der Installer prüft alle Textänderungen vor dem Schreiben. Vorhandene geänderte Dateien werden in einem datierten Nachbarordner gesichert. Wiederholtes Ausführen ändert nichts. Er ersetzt keine kompletten bestehenden Projektdateien und berührt weder die Windows-Setup-Skripte noch die Generatoren. Eigene Änderungen außerhalb der betroffenen Stellen bleiben erhalten. Bei unbekanntem Dateistand bricht er ab.

3. Auf einem neuen PC zuerst das separat vorhandene `setup_windows.cmd` erfolgreich abschließen, damit MAVLink-/DroneCAN-Header erzeugt sind. Diese Erweiterung löst keine noch bestehenden Generatorfehler.
4. In PlatformIO → Project Tasks das passende Ziel wählen, zuerst Build, dann Upload:

| Rolle | Environment |
|---|---|
| TX, BLE-Sensoren und USB-Freitext | `tx-heltec-v2-868-thingy53` |
| RX, Status- und Textdisplay | `rx-heltec-v2-868` |

Alternativ im Projektterminal:
```powershell
& "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe" run -e tx-heltec-v2-868-thingy53
& "$env:USERPROFILE\.platformio\penv\Scripts\platformio.exe" run -e rx-heltec-v2-868
```
Für Upload jeweils `-t upload --upload-port COMxx` mit dem tatsächlichen Anschluss ergänzen. Nur den gewählten Empfänger/Sender flashen. Antenne vor Funkbetrieb anschließen.

## Verhalten und Pins

Der TX verwendet die vorhandene BLE-Brücke für Thingy:53 und Dongles mit Geräte-ID. Die Thingy-Firmware bleibt unverändert. USB-Freitext läuft wie bisher mit 115200 Baud. Der RX übernimmt die bestehende Status-/Textanzeige mit automatischem Seitenwechsel. Defaults: Bindphrase `da1twd`, SX1276-Modus `MODE_19HZ_7X`, transparenter Datenkanal. Bereits gespeicherte Einstellungen können Defaults übersteuern; beide Funkseiten müssen zueinander passende Einstellungen haben.

| Funktion | GPIO |
|---|---|
| SX1276 SCK / MISO / MOSI / CS | 5 / 19 / 27 / 18 |
| SX1276 Reset / DIO0 | 14 / 26 |
| OLED SDA / SCL / Reset | 4 / 15 / 16 |
| Vext einschalten | 21, LOW |
| Status-LED | 25 |
| USB-UART TX / RX | 1 / 3 |
| TX: CLI beim Start auswählen | 22 an GND beim Reset; sonst offen |

OLED-Stromversorgung und Reset werden vor der Displayinitialisierung gesetzt. PRG wird nicht als Bindetaste verwendet. LED-Verhalten entspricht dem bisherigen TTGO-Ziel (keine zusätzliche Dimmung in dieser Erweiterung).

Offizielle Pinbelegung: https://resource.heltec.cn/download/WiFi_LoRa_32/WIFI_LoRa_32_V2.pdf

## Ersttest

Zuerst zwei V2 mit passenden TX/RX-Zielen testen: OLED, Funkverbindung, USB-Testtext, dann BLE-Sensorwerte. Nach Ausschalten/Einschalten Wiederverbindung prüfen. Das Testskript am PC oder nRF Connect muss seine Sensorverbindung freigeben, bevor der TX verbinden kann.

## Rücknahme und Git

Der Sicherungsordner enthält Originaldateien mit relativen Pfaden. Für Rücknahme diese zurückkopieren und die in `NEUE_DATEIEN.txt` genannten neu angelegten Dateien entfernen. Nicht pauschal das Projekt löschen.

Nach erfolgreichem Hardwaretest `git diff` und `git status --short` prüfen, gezielt Änderungen committen und pushen. Build-Verzeichnisse und lokale Sicherungen nicht committen.

## Prüfung am 26.11.2026

- Beide Firmware-Builds erfolgreich unter Linux, PlatformIO Core 6.2.0, espressif32 6.13.0, Arduino-ESP32 2.0.17, NimBLE 1.4.3.
- TX: 748369 Byte Flash, 49820 Byte statischer RAM; RX: 375317 Byte Flash, 32700 Byte statischer RAM. Dynamische BLE-Speicherbelegung wird damit nicht gemessen.
- Installer getestet: Pfade mit Leerzeichen, Wiederholung ohne Änderungen, Erhalt eigener Änderungen und Abbruch vor dem Schreiben bei unbekanntem Stand.
- Bestehende PlatformIO-Environment-Konfigurationen unverändert; vorhandene BLE-Zeilen- und Textmultiplexer-Tests bestanden.
- Nicht auf physischer V2-Hardware und nicht unter Windows ausgeführt. Funk, OLED, BLE und USB sind nach dem Upload am Gerät zu prüfen.
