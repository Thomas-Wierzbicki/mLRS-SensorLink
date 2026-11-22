# Heltec WiFi LoRa 32 V4.3: TX und RX

Portierung für zwei V4.3-Boards mit ESP32-S3R2, SX1262 und KCT8103L,
16 MB Flash und 2 MB Quad-PSRAM. Bestehende TTGO-Ziele bleiben erhalten.
Basis: Thomas-Wierzbicki/mLRS-TTGO, Commit
`bec3f4d9f3dbe2ac098477ff505291f42c75f31e`.

## Voraussetzungen

Im bereits funktionierenden Projekt sind die generierten MAVLink-Dateien
vorhanden. Bei einem frischen Klon zuerst die normale Projektvorbereitung
mit `python run_setup.py` ausführen. Fehlt beim Build
`out/mlrs_all/mlrs_all.h`, wurde dieser Vorbereitungsschritt noch nicht erledigt.

## Build und Upload in VS Code

1. Projektordner öffnen. PlatformIO neu laden, falls neue Ziele fehlen.
2. PlatformIO > Project Tasks > `tx-heltec-v43-868-thingy53` > General > Build.
3. TX-Board mit passender 868-MHz-Antenne und USB-Datenkabel anschließen.
4. Unter demselben Ziel Upload wählen. Zunächst nur dieses Board am PC anschließen.
5. RX entsprechend mit `rx-heltec-v43-868` bauen und hochladen.

Alternative im **PlatformIO-Terminal**:

```powershell
pio run -e tx-heltec-v43-868-thingy53
pio run -e rx-heltec-v43-868
pio run -e tx-heltec-v43-868-thingy53 -t upload
pio run -e rx-heltec-v43-868 -t upload
```

Die Heltecs verwenden natives USB; neue COM-Nummern sind normal. COM9/COM8
sind nicht fest vorgegeben. Falls Upload nicht startet: PRG gedrückt halten,
RST kurz drücken, PRG loslassen und Upload erneut starten. PRG beim normalen
Einschalten nicht gedrückt halten. Antenne vor Betrieb anschließen.

## Funktionen und erste Prüfung

- TX übernimmt die vorhandene BLE-Bridge: unverändertes Thingy:53 und bis zu
  zwei Dongles mit dem vorhandenen Geräte-ID-Dienst.
- USB-Freitext bleibt parallel möglich, mit den vorhandenen Python-Skripten
  und der neuen COM-Nummer. Nur ein Programm darf den Port öffnen.
- RX zeigt Funkstatus und Text; Anzeigewechsel wie bisher alle 15 Sekunden.
- Beide Heltec-Builds starten mit 868 MHz, Modus 19 Hz, Bind-Phrase `da1twd`,
  transparentem seriellen Kanal und RX-Baudrate 115200. Gespeicherte Parameter
  können die Compile-Defaults überschreiben.
- Die Thingy- und Dongle-Firmware wird nicht verändert.
- Für diesen Test beide Heltecs verwenden; das vorhandene TTGO-Paar kann
  mit seinen bisherigen Build-Zielen weiterbetrieben werden.

Prüfen: beide OLEDs starten, Verbindung wird angezeigt, Sensorzeilen kommen
am RX an, USB-Freitext kommt an, danach Verbindung nach Stromunterbrechung
wiederherstellen. Abschließend beide Geräte ohne USB-PC-Verbindung betreiben.
Nicht direkt nebeneinander testen, einige Meter Abstand verwenden.

## Hardwaredetails

| Funktion | GPIO / Einstellung |
|---|---|
| SX1262 NSS/SCK/MISO/MOSI | 8 / 9 / 11 / 10 |
| SX1262 RESET/BUSY/DIO1 | 12 / 13 / 14 |
| TCXO | DIO3, 1,8 V |
| FEM Versorgung / CSD / CTX | 7 / 2 / 5 |
| FEM CPS | SX1262 DIO2, automatische RF-Umschaltung |
| OLED SDA/SCL/RESET | 17 / 18 / 21 |
| Vext | 36, aktiv Low |
| LED / PRG | 35 / 0 |
| TX CLI statt Datenkanal | GPIO4 beim Start mit GND verbinden |

FEM RX: CSD=1, CTX=0 (LNA). TX: CSD=1, CTX=1, CPS wird durch DIO2 gesetzt.
Der RSSI ist der Wert des SX1262 hinter dem LNA, keine kalibrierte Messung
am Antennenanschluss.

Zum Einstieg sind nur niedrige Leistungsstufen vorgesehen: SX1262 -9, -3
und 0 dBm. Die angezeigten 4/10/13 dBm bzw. 3/10/20 mW verwenden eine
**vorläufige Gain-Annahme von 13 dB**; sie sind keine gemessenen Ausgangswerte.
Default ist die niedrigste Stufe. Die volle beworbene 28-dBm-Leistung ist
in diesem Build nicht freigegeben. Kalibrierung am realen Board steht aus.

USB-Ausgabe ist nicht blockierend: Bei abgezogenem Host oder vollem USB-Puffer
können USB-Ausgabebytes verworfen werden, damit die Funkverarbeitung weiterläuft.
Dieser erste Port ist auf Sensor-/Textbetrieb ausgelegt, nicht auf verlustfreies
USB-Logging bei beliebiger Datenrate. GPS, Solarüberwachung und Akkuanzeige
sind nicht Bestandteil dieser Änderung.

## Referenzen

- https://wiki.heltec.org/docs/devices/open-source-hardware/esp32-series/lora-32/wifi-lora-32-v4/
- https://github.com/HelTecAutomation/HeltecWiKi/blob/master/news/lna/lna.md
- https://resource.heltec.cn/download/WiFi_LoRa_32_V4/Schematic/HTIT-WB32LAF_V4.3.pdf
- https://github.com/meshtastic/firmware/blob/master/variants/esp32s3/heltec_v4/variant.h
- https://github.com/meshtastic/firmware/blob/master/src/mesh/LoRaFEMInterface.cpp

Hardwaretest einschließlich Funk, OLED, BLE und USB steht noch aus.
