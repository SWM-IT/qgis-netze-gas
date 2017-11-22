==================================================
*Geogig Local Client: Vereinfachtes Geogig Plugin*
==================================================

:Autor: Markus Hesse
:Date: $Date: 2017-11-22 10:17:45 +0000 (Wed, 22 Nov 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Voraussetzungen, Installation und Handhabung

Einleitung
----------

Das *Vereinfachte Geogig Plugin* stellt eine Alternative zum vorhandenen Geogig Plugin dar (vgl. https://github.com/boundlessgeo/qgis-geogiglight-plugin). Es ist für die tägliche Arbeit eines Efassers konzipiert. Er kann damit:

- Änderungen einchecken zwischen den lokalen GeoPackage Datenbanken und dem Serverrepository synchronisieren.
- Änderungen verfolgen und Konflikte bearbeiten.
- Branches anlegen und zwischen den Branches navigieren.

Ausdrücklich nicht vorgesehen sind adminsitrative Arbeiten wie:

- Konfiguration der Verbindung zum Server sowie des/der Repositories.
- Herunterladen der gewünschten Layer zum aktuellen Projekt.

Gegenüber dem vorhandenen Geogig Plugin gibt es folgende Vereinfachungen für den Benutzer:

- Der aktuelle zuletzt gewählte Branch wird persitent gespeichert. Er steht auch nach einem Neustart zur Verfügung.
- Ein Commit wird immer in den aktuellen Branch gemacht.
- Merges von und zu dem aktuellen Branch sind nur zu einem für den jeweiligen Branch definierten übergeordneten Branch möglich. (Geogig erlaubt das Merggen zwischen beliebigen Branches.)
- Alle Commit- und Mergeoperationen sowie die Navigation zwischen den Branches werden immer auf allen Layern des jeweiligen Repositories ausgeführt. (Mit dem vorhandenen Geogig Plugin muss das für jeden Layer einzeln gemacht werden.)



Voraussetzungen
---------------

Um das *Vereinfachte Geogig Plugin* verwenden zu können, benötigen Sie einen Geogig Server, der die zu bearbeitenden Repositories bereitstellt. Zu dessen Installation lesen Sie bitte:

- http://geogig.org/docs/index.html

und insbesondere

- http://geogig.org/docs/interaction/networking.html


Installation der Plugins
------------------------ 

Installieren Sie zunächst die beiden zugrundeliegenden Geogig Plugins aus

- https://github.com/boundlessgeo/lib-qgis-commons
- https://github.com/boundlessgeo/qgis-geogiglight-plugin

Im Detail:

*lib-qgis-commons*: 

- Download der Sourcen von https://github.com/boundlessgeo/lib-qgis-commons
- Kopie von ..\lib-qgis-commons\qgiscommons2 ins QGis Pluginverzeichnis (c:\Users\<user>\.qgis2\python\plugins)

*qgis-geogiglight-plugin*

- Download der Sourcen von https://github.com/boundlessgeo/qgis-geogiglight-plugin
- Installation gemäß der Anleitung auf der oben genannten Seite (also einmalig Installation von ``paver``, dann ``paver setup`` und ``paver install``)

Dann installieren Sie das Vereinfachtes Geogig Plugin.

- Download von https://github.com/SWM-IT/qgis-netze-gas
- Kopie des Verzeichnisses ...\qgis-netze-gas\source\examples\python\plugins\GeogigLocalClient ins QGis Pluginverzeichnis (c:\Users\<user>\.qgis2\python\plugins)


Schalten Sie im QGis die Plugins *GeoGig Client* und *Geogig Local Client* aktiv: ``Erweiterungen\Erweiterungen verwalten und installieren...'', Suche nach geogig, Häckchen vor den jeweilgen Plugins anhaken.


Vorbereitung eines Repositiories
--------------------------------

Verwenden Sie das zugrundeliegenden Geogig Plugin um die Verbindung zum Geogig Server sowie das gewünschte Geogig Repository zu konfigurieren. Danach sollten sie die gewünschten Layer vom Geogig Server herunterladen und Ihrem Projekt hinzufügen. Zu den Details der Bedienung des Plugins siehe https://github.com/boundlessgeo/qgis-geogiglight-plugin/blob/master/docs/source/usage.rst.


Arbeiten mit dem Plugin
-----------------------

Starten Sie das Plugin mittels ``Datenbank\Geogig Local Client\GeoGig Manager`` oder über das Symbol ``GeoGig Manager`` in der Toolbar.
Es öffnet sich folgender Dialog:

 .. image:: images/geogig/GeoGigManagerDialog.png


Mit den beiden Pulldownmenüs in der ersten Zeile können sie den Geogig Server sowie das gewünschen Repository auswählen. Diese müssen natürlich zuvor konfiguriert worden sein (vgl. ``Vorbereitung eines Repositiories``).

Die weiteren Knöpfe der ertsen Zeile haben folgende Funktionen:

| |BtnSync|       : Synchronisiert locale Änderungen und Änderungen auf dem Server.
| |BtnMergeDown|  : Merged Änderungen des übergeordneten Branches zum aktuellen Branch
| |BtnMergeUp|    : Merged Änderungen des aktuellen Branches zum übergeordneten Branch
| |BtnRevert|     : Löscht lokale Änderungen, die noch nicht zum Server gesandt wurden
| |BtnShowChanges|: Zeigt lokale Änderungen an, die noch nicht zum Server gesandt wurden

.. |BtnSync|        image:: images/geogig/BtnSync.PNG
.. |BtnMergeDown|   image:: images/geogig/BtnMergeDown.PNG
.. |BtnMergeUp|     image:: images/geogig/BtnMergeUp.PNG
.. |BtnRevert|      image:: images/geogig/BtnRevert.PNG
.. |BtnShowChanges| image:: images/geogig/BtnShowChanges.PNG


