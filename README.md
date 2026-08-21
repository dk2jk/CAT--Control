<h1>Anwendung der CAT- Schnittstelle mit Beispielen für RaspberryPi, PC und ESP32.</h1>

Programmiersprache ist Python.<br>
Verwendete Geräte: IC-705 , Elecraft KXPA und Yaesu FT-710.

Dieses Projekt zeigt die Steuerung von Amateurfunkgeräten über die CAT-Schnittstelle (Computer Aided Transceiver). Die Skripte wurden auf einem Linux-Laptop entwickelt und für den Einsatz auf einen Raspberry Pi sowie einen ESP32 portiert.
Die Python-Skripte sind klein gehalten, um die reine CAT-Kommunikation verständlich zu zeigen.

<li><b>1. Frequenzabfrage beim Icom IC-705 (Raspberry Pi / PC)</li></b>
Ein Python- Skript liest die aktuelle Frequenz des IC-705 über das CI-V Protokoll (Hexadezimal-Befehle) aus. Mit dieser Information können nachgeschaltete Antennenschalter oder Endstufen (wie die Elecraft KXPA) automatisch das richtige Band wählen.<br>
<li><b>2. Yaesu FT-710 "Tune-Button" via CAT</li></b>
    Das Yaesu CAT-Protokoll basiert auf lesbaren ASCII-Klartextbefehlen, die mit einem Semikolon (;) abgeschlossen werden. Der "Tune-Button" setzt eine Kette von Befehlen ab: Wechsel in den RTTY-Modus, Träger setzen (PTT), Tuner aktivieren und zurück in den Ausgangszustand.<br>
<li><b>2a. USB-Schnittstelle am PC</li></b>
    Der Tune-Button besteht aus eine Icon auf dem Desktop, Programmiersprache: <i>Python</i>
<li><b>2b. UART am ESP-32 Microcontroller</li></b>
Auf dem ESP32 wird eine UART-Schnittstelle mit TTL-Pegel verwendet, die über einen Pegelwandler  5V / 3,3V
mit dem Transceiver verbunden ist. Programmiersprache: <i>MicroPython</i>

