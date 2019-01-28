Plugin: EditorParser

Das Plugin in das Verzeichnis "C:\Users\<USERNAME>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins" ablegen.
Danach QGIS ggf. neu starten. Im QGIS über Erweiterungen => Erweiterungen verwalten
und installieren das Plugin EditorParser suchen und installieren.

Das Plugin ist danach unter Datenbank => EditorParser oder über das Icon in der Toolbar zu finden.    


Funktion Plugin
---------------
Das Plugin wandelt die Layernamen um und erstellt die dazugehörigen Formularsichtbarkeiten für die einzelnen
Layer anhand der ausgespielten Smallworld Sichtbarkeiten aus den gced Tabellen.

Vorgehensweise
--------------
Um die geöffnete Projektdatei zu konvertieren starten Sie den Vorgang einfach über den Button
"Start Konvertierung über geöffnete Projektdatei" und folgen den Anweisungen. Danach muss das Projekt einmal händisch gespeichert
werden, sodass die Änderungen übernommen werden.

Konfiguration
-------------
Die Zugangsdaten zur Datenbank sind in der Datei config.cfg im Verzeichnis EditorParser abzulegen:
[Connection]
host=dbhost
port=5432
dbname=dbname
user=username
password=secret

Debugging
---------
Um ein Debugging gegen localhost zu ermöglichen, müssen die folgenden Umgebungsvariablen gesetzt sein.
Dies kann in QGIS zB. wie folgt geschehen: Einstellungen -> Optionen -> System -> Umgebung -> benutzerdefinierte Umgebungsvariablen verwenden
(vgl. __init__.py):
PY_DEBUG_FLAG: Der Wert "True" startet das Debugging
PY_DEBUG_EGG: Pfad zur Debug-Egg-Datei von PyCharm Professional
PY_DEBUG_PORT: Port, auf den der externe Debugserver läuft