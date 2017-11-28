========================
*Geogig Package Creator*
========================

:Autor: Markus Hesse
:Date: $Date: 2017-11-28 15:17:45 +0000 (Wed, 22 Nov 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Handhabung

Einleitung
----------

Der *Geogig Package Creator* dient zur Erstellung von gepackten Dateien (zip) mit allem Notwendigen zur Bearbeitung von Daten mittes QGis unter Zuhilfenahme von Geogig und des *Vereinfachtes Geogig Plugin*. Hiermit kann ein Administrator Daten und Konfiguration für seine Benutzer auf bequeme Weise bereitstellen.
Die erstellen Packe kannn ein Benutzer per *Geogig Package Reader* auf seinem System auspacken und hat ein fertig konfiguriertes System zur Hand.

Ein Packet enthält folgende Komponenten:

- Datenbanken (also GeoPackage Dateien)
- Geogig Konfiguration (Konfiguration des Geogig Servers, der Repositiories sowie der durch Geogig verwalteten Layer)
- Zusätztliche Plugins, also Geogig Plugin und *Vereinfachtes Geogig Plugin*
- QGis Projekt


Installation der Plugins
------------------------ 

Bevor Sie den *Geogig Package Creator* installieren, müssen Sie das *Vereinfachtes Geogig Plugin* sowie dessen Voraussetzungen installieren (siehe Dokumentation GeogigLocalClient.rst).

Installieren Sie dann den *Geogig Package Creator*:

- Download von https://github.com/SWM-IT/qgis-netze-gas
- Kopie des Verzeichnisses ...\\qgis-netze-gas\\source\\examples\\python\\plugins\\GeogigPackageCreator ins QGis Pluginverzeichnis (c:\\Users\\<user>\\.qgis2\\python\\plugins)

Schalten Sie im QGis die Plugins *Geogig Package Creator* aktiv: ``Erweiterungen\Erweiterungen verwalten und installieren...'', Suche nach geogig, Häkchen vor dem Plugin anhaken.


Handhabung
----------

Starten Sie das Plugin mittels ``Datenbank\Geogig Package\Create Package`` oder über das Symbol ``Create Package`` in der Toolbar.
Es öffnet sich folgender Dialog:

 .. image:: images/geogig/GeoGigPackageCreatorDialog.png


Im Editfeld geben Sie den Pfad und den Dateinamen des zu erzeugenden Paketes an. Mit dem Knopf an der rechten Seite öffnen Sie eine Dateiauswahlbox, mit der Sie das u.U. einfacher bewerkstelligen können.

Darunter gibt es vier Checkboxen, über die Sie steuern können, welche Komponenten das Paket enthalten soll. Standardmäßig sind alle Boxen angehakt.

Der Knopf ``Cancel`` beendet den Dialog ohne dass eine Aktion ausgelöst wird. Der Knpf ``OK`` startet die Erstellung des Paketes. In der Progressbar können Sie den Fortschritt der Paketerstellung verfolgen.


