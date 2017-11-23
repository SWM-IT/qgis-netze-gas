==================================================
*Geogig Local Client: Vereinfachtes Geogig Plugin*
==================================================

:Autor: Markus Hesse
:Date: $Date: 2017-11-22 10:17:45 +0000 (Wed, 22 Nov 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Voraussetzungen, Installation und Handhabung

Einleitung
----------

Das *Vereinfachte Geogig Plugin* stellt eine Alternative zum vorhandenen Geogig Plugin dar (vgl. https://github.com/boundlessgeo/qgis-geogiglight-plugin). Es ist für die tägliche Arbeit eines Erfassers konzipiert. Er kann damit:

- Änderungen einchecken zwischen den lokalen GeoPackage Datenbanken und dem Serverrepository synchronisieren.
- Änderungen verfolgen und Konflikte bearbeiten.
- Branches anlegen und zwischen den Branches navigieren.

Ausdrücklich nicht vorgesehen sind administrative Arbeiten wie:

- Konfiguration der Verbindung zum Server sowie des/der Repositories.
- Herunterladen der gewünschten Layer zum aktuellen Projekt.

Gegenüber dem vorhandenen Geogig Plugin gibt es folgende Vereinfachungen für den Benutzer:

- Der aktuelle, zuletzt gewählte Branch wird persistent gespeichert. Er steht auch nach einem Neustart zur Verfügung.
- Ein Commit wird immer in den aktuellen Branch gemacht.
- Merges von und zu dem aktuellen Branch sind nur zu einem für den jeweiligen Branch definierten übergeordneten Branch möglich. (Geogig erlaubt das Mergen zwischen beliebigen Branches.)
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
- Kopie von ..\\lib-qgis-commons\\qgiscommons2 ins QGis Pluginverzeichnis (c:\\Users\\<user>\\.qgis2\\python\\plugins)

*qgis-geogiglight-plugin*

- Download der Sourcen von https://github.com/boundlessgeo/qgis-geogiglight-plugin
- Installation gemäß der Anleitung auf der oben genannten Seite (also einmalig Installation von ``paver``, dann ``paver setup`` und ``paver install``)

Dann installieren Sie das Vereinfachtes Geogig Plugin.

- Download von https://github.com/SWM-IT/qgis-netze-gas
- Kopie des Verzeichnisses ...\\qgis-netze-gas\\source\\examples\\python\\plugins\\GeogigLocalClient ins QGis Pluginverzeichnis (c:\\Users\\<user>\\.qgis2\\python\\plugins)


Schalten Sie im QGis die Plugins *GeoGig Client* und *Geogig Local Client* aktiv: ``Erweiterungen\Erweiterungen verwalten und installieren...'', Suche nach geogig, Häkchen vor den jeweiligen Plugins anhaken.


Vorbereitung eines Repositiories
--------------------------------

Verwenden Sie das zugrundeliegenden Geogig Plugin um die Verbindung zum Geogig Server sowie das gewünschte Geogig Repository zu konfigurieren. Danach sollten sie die gewünschten Layer vom Geogig Server herunterladen und Ihrem Projekt hinzufügen. Zu den Details der Bedienung des Plugins siehe https://github.com/boundlessgeo/qgis-geogiglight-plugin/blob/master/docs/source/usage.rst.


Arbeiten mit dem Plugin
-----------------------

Starten Sie das Plugin mittels ``Datenbank\Geogig Local Client\GeoGig Manager`` oder über das Symbol ``GeoGig Manager`` in der Toolbar.
Es öffnet sich folgender Dialog:

 .. image:: images/geogig/GeoGigManagerDialog.png


Mit den beiden Pulldownmenüs in der ersten Zeile können Sie den Geogig Server sowie das gewünschte Repository auswählen. Diese müssen natürlich zuvor konfiguriert worden sein (vgl. ``Vorbereitung eines Repositiories``).

Die weiteren Knöpfe der ersten Zeile haben folgende Funktionen:

| |BtnSync|       : Synchronisiert lokale Änderungen des aktuellen Branches und Änderungen auf dem Server.
| |BtnMergeDown|  : Merge Änderungen des übergeordneten Branches zum aktuellen Branch
| |BtnMergeUp|    : Merge Änderungen des aktuellen Branches zum übergeordneten Branch
| |BtnRevert|     : Löscht lokale Änderungen, die noch nicht zum Server gesandt wurden
| |BtnShowChanges|: Zeigt lokale Änderungen an, die noch nicht zum Server gesandt wurden

.. |BtnSync|        image:: images/geogig/BtnSync.PNG
.. |BtnMergeDown|   image:: images/geogig/BtnMergeDown.PNG
.. |BtnMergeUp|     image:: images/geogig/BtnMergeUp.PNG
.. |BtnRevert|      image:: images/geogig/BtnRevert.PNG
.. |BtnShowChanges| image:: images/geogig/BtnShowChanges.PNG


Unter der Knopfzeile befindet sich das Fenster mit dem Branch Tree. Die Wurzel aller Branches ist ``master``. Von hier können untergeordnete Branches hierarchisch angelegt werden. Der aktuelle Branch ist durch einen fette und etwas größere Schrift hervorgehoben (im Snapshot oben ``B6``).
Durch einen Rechtsklick auf einen Branch erhalten Sie folgendes Popupmenü:

 .. image:: images/geogig/BranchesPulldown.PNG

Die Funktionen darin sind:

- **Goto this Branch**: Gehe mit allen Layern des Repositories zu diesem Branch und wähle diesen als aktuellen Branch. Eine Progressbar oberhalb der Karte zeigt den Fortschritt dieser Aktion (für jeden veränderten Layer, geht es einen Schritt weiter). Der gewählte Branch wird danach fett und mit etwas größeren Buchstaben als aktueller Branch dargestellt. Merge- ind Synchronisationsaktionen beziehen sich nun auf diesen Branch.
- **Create branch**: Erzeugt einen Unterbranch zum gewählten Branch. Beachte: Man kann auch einen Unterbranch zu einem anderen Branch als dem aktuellen Branch erzeugen!
- **Delete branch**: Lösche den gewählten Branch. Beachte: Der gewählte Branch muss nicht der aktuelle Branch sein. Ein Löschen von ``master`` ist nicht möglich. Besitzt ein Branch Unterbranches, so erfolgt eine zusätzliche Rückfrage an den Benutzer. Falls er zustimmt, wird der gewählte Branch und seine Unterbranches gelöscht.

Anmerkung zur Branchhierarchie:

	  In Geogig gibt es eigentlich keine Hierarchie unter den Branches. Alle Branches sind gleichberechtigt und daher kann der Benutzer auch von jedem Branch in jeden Branch mergen. Um die Bedienbarkeit des Plugins jedoch zu vereinfachen, haben wir hier eine Hierarchie eingefügt. Technisch wird das über eine Namenskonvention erreicht: Der Wurzelbranch ist ``master``. Branches mit "einfachen" Namen sind master direkt untergeordnet. Ein Branch darunter hat den Namane seines übergeordneten Branches mit folgender Notation im Namen eingebaut: "<eigener Name>_($<übergeordneter Branch$)". Im Plugin wird nur der <eigene Name> angezeigt.

Unter dem Fenster mit dem Branchtree liegt das Fenster mit der Commithistorie. Wird im oberen Fenster ein Branch ausgewählt, so wird in diesem Fenster die Liste der Commits zu diesem Branch angezeigt. Durch einen Rechtsklick auf einen Commit erhalten Sie folgendes Pulldownmenü:

 .. image:: images/geogig/CommitsPulldown.PNG

Die Funktionen darin sind:

- **Create branch from this commit**: Erzeugt einen Unterbranch zum ausgewählten Branch basierend auf dem selektierten Commit.
- **Show changes of this commit**: Öffnet ein neues Menü mit allen Änderungen, die mit diesem Commit abgespeichert wurden.
- **Show details of this commit**: Öffnet ein neues Menü mit Informationen zu diesem Commit, u.a. Autor und Datum.
- **Create tag**: Erzeugt einen Tag zu diesem Commit
- **Delete tag**: Löscht alle Tags, die diesem Commit angehängt waren.
	  




