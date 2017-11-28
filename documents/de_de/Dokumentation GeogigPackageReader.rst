=======================
*Geogig Package Reader*
=======================

:Autor: Markus Hesse
:Date: $Date: 2017-11-28 15:17:45 +0000 (Wed, 22 Nov 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Handhabung

Einleitung
----------

Der *Geogig Package Reader* dient zum Laden von Paketen, die mit dem *Geogig Package Creator* erstellt wurden.


Installation der Plugins
------------------------ 

Installieren Sie den *Geogig Package Reader* wie folgt:

- Download von https://github.com/SWM-IT/qgis-netze-gas
- Kopie des Verzeichnisses ...\\qgis-netze-gas\\source\\examples\\python\\plugins\\GeogigPackageReader ins QGis Pluginverzeichnis (c:\\Users\\<user>\\.qgis2\\python\\plugins)

Schalten Sie im QGis die Plugins *Geogig Package Reader* aktiv: ``Erweiterungen\Erweiterungen verwalten und installieren...'', Suche nach geogig, Häkchen vor dem Plugin anhaken.

Der *Geogig Package Reader* kann für sich allein installiert werden. Er benötigt keine weiteren Plugins als Voraussetzung.


Handhabung
----------

Starten Sie das Plugin mittels ``Datenbank\Geogig Package\Open Package`` oder über das Symbol ``Open Package`` in der Toolbar.
Es öffnet sich folgender Dialog:

 .. image:: images/geogig/GeoGigPackageReaderDialog.png


Im Editfeld geben Sie den Pfad und den Dateinamen des zu ladenden Paketes an. Mit dem Knopf an der rechten Seite öffnen Sie eine Dateiauswahlbox, mit der Sie das u.U. einfacher bewerkstelligen können.

Der Knopf ``Cancel`` beendet den Dialog ohne dass eine Aktion ausgelöst wird. Der Knpf ``OK`` startet das des Paketes. In der Progressbar können Sie den Fortschritt verfolgen.

Sofern alle Komponenten im Paket enthalten sind, geschieht folgendes:

- Die Datenbanken (GeoPackages) werden nach ``c:\ProgramData\geogig\repos\`` entpackt.
- Die Projektdatei wird ins Verzeichnis ``c:\ProgramData\geogig\qgis\`` entpackt.
- Die GeoGig Konfigurationsdateien werden ins Verzeichnis ``c:\Users\<User>\geogig\`` entpackt.
- Die Plugins werden ins QGis Plugin Verzeichnis (normalerweise c:\\Users\\<user>\\.qgis2\\python\\plugins) entpackt.
- Die Plugins *geogig* und *GeogigLocalClient* werden geladen und aktiviert.
- Das QGis Projekt wird gestartet.
