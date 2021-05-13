# Datenbanken_Sem4_3471119
Projekt Datenbanken
Matrikelnummer: 3471119
## Themenübersicht
* Zeitreihendatenbank __InfluxDB__ (1.8.4)
* Verbindung über __Python__ aufbauen
* Datensatz von Kaggle
  * __COVID-19 World Vaccination Progress__
* Datensatz als CSV über Python in Datenbank laden
* Tool __Grafana__ zur Auswertung
  * Holt über Querys direkt die Daten von der Datenbank
## Installation
### Requirements
* Kaggle API Key
  * https://www.kaggle.com -> anmelden -> Profilbild -> "Account" -> "API" -> "Create New API Token" ---> downloads: kaggle.json
* InfluxDB 1.8.4 oder neue 1.x
  * https://portal.influxdata.com/downloads/
* Python version 3.8.5 oder neuer
  * https://www.python.org/downloads/
### Anleitung
1. git clone https://github.com/JuBa-git/Datenbanken_Sem4_3471119.git InfluxPy
2. config_template.py kopieren nach config.py
3. username & key aus kaggle.json in config.py übernehmen
4. für InfluxDB (Window): Die Datei "influxdb.conf" in dem ausgepackten Ordner "influxdb-VERSION" bearbeiten -> Pfade für "Data", "Meta" und "Wal" angeben. Bsp.: dir = "data" [Tipp: suchen nach "/data", etc.]. Dort kann man auch noch "reporting-disabled = false" -> "... = true" setzen.
5. Server starten: z.B.: aus Homeverzeichnis: "PFAD/ZU/influxd run -config PFAD/ZU/influxdb.conf"
6. "influx" im Verzeichnis "influxdb-VERSION" starten -> InfluxDB shell
7. Darin eine Datenbank und einen User anlegen mit den Befehlen:
    > CREATE DATABASE <myDB>
    > CREATE USER admin WITH PASSWORD '<password>' WITH ALL PRIVILEGES
9. Name der Datenbank, den Host "localhost", den User "admin" und das Passwort in die config.py übernehmen
10. Python installieren und die Module influxdb und kaggle installieren: pip install influxdb kaggle
11. kaggleToInflux.py ausführen z.B. mit: python kaggleToInflux.py
