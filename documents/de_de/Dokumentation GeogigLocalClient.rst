==================================================
*Geogig Local Client: Vereinfachtes Geogig Plugin*
==================================================

:Autor: Markus Hesse
:Date: $Date: 2017-11-22 10:17:45 +0000 (Wed, 22 Nov 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Voraussetzungen, Installation und Handhabung

Einleitung
----------

Das *Vereinfachte Geogig Plugin* stellt eine Alternative zum vorhandenen Geogig Plugin dar (vgl. https://github.com/boundlessgeo/qgis-geogiglight-plugin). Es ist f�r die t�gliche Arbeit eines Erfassers konzipiert. Er kann damit:

- �nderungen einchecken zwischen den lokalen GeoPackage Datenbanken und dem Serverrepository synchronisieren.
- �nderungen verfolgen und Konflikte bearbeiten.
- Branches anlegen und zwischen den Branches navigieren.

Ausdr�cklich nicht vorgesehen sind administrative Arbeiten wie:

- Konfiguration der Verbindung zum Server sowie des/der Repositories.
- Herunterladen der gew�nschten Layer zum aktuellen Projekt.

Gegen�ber dem vorhandenen Geogig Plugin gibt es folgende Vereinfachungen f�r den Benutzer:

- Der aktuelle, zuletzt gew�hlte Branch wird persistent gespeichert. Er steht auch nach einem Neustart zur Verf�gung.
- Ein Commit wird immer in den aktuellen Branch gemacht.
- Merges von und zu dem aktuellen Branch sind nur zu einem f�r den jeweiligen Branch definierten �bergeordneten Branch m�glich. (Geogig erlaubt das Mergen zwischen beliebigen Branches.)
- Alle Commit- und Mergeoperationen sowie die Navigation zwischen den Branches werden immer auf allen Layern des jeweiligen Repositories ausgef�hrt. (Mit dem vorhandenen Geogig Plugin muss das f�r jeden Layer einzeln gemacht werden.)



Voraussetzungen
---------------

Um das *Vereinfachte Geogig Plugin* verwenden zu k�nnen, ben�tigen Sie einen Geogig Server, der die zu bearbeitenden Repositories bereitstellt. Zu dessen Installation lesen Sie bitte:

- http://geogig.org/docs/index.html

und insbesondere

- http://geogig.org/docs/interaction/networking.html


Installation der Plugins
------------------------ 

Installieren Sie zun�chst die beiden zugrundeliegenden Geogig Plugins aus

- https://github.com/boundlessgeo/lib-qgis-commons
- https://github.com/boundlessgeo/qgis-geogiglight-plugin

Im Detail:

*lib-qgis-commons*: 

- Download der Sourcen von https://github.com/boundlessgeo/lib-qgis-commons
- Kopie von ..\\lib-qgis-commons\\qgiscommons2 ins QGis Pluginverzeichnis (c:\\Users\\<user>\\.qgis2\\python\\plugins)

*qgis-geogiglight-plugin*

- Download der Sourcen von https://github.com/boundlessgeo/qgis-geogiglight-plugin
- Installation gem�� der Anleitung auf der oben genannten Seite (also einmalig Installation von ``paver``, dann ``paver setup`` und ``paver install``)

Dann installieren Sie das Vereinfachtes Geogig Plugin.

- Download von https://github.com/SWM-IT/qgis-netze-gas
- Kopie des Verzeichnisses ...\\qgis-netze-gas\\source\\examples\\python\\plugins\\GeogigLocalClient ins QGis Pluginverzeichnis (c:\\Users\\<user>\\.qgis2\\python\\plugins)


Schalten Sie im QGis die Plugins *GeoGig Client* und *Geogig Local Client* aktiv: ``Erweiterungen\Erweiterungen verwalten und installieren...'', Suche nach geogig, H�kchen vor den jeweiligen Plugins anhaken.


Vorbereitung eines Repositiories
--------------------------------

Verwenden Sie das zugrundeliegenden Geogig Plugin um die Verbindung zum Geogig Server sowie das gew�nschte Geogig Repository zu konfigurieren. Danach sollten sie die gew�nschten Layer vom Geogig Server herunterladen und Ihrem Projekt hinzuf�gen. Zu den Details der Bedienung des Plugins siehe https://github.com/boundlessgeo/qgis-geogiglight-plugin/blob/master/docs/source/usage.rst.


Arbeiten mit dem Plugin
-----------------------

Starten Sie das Plugin mittels ``Datenbank\Geogig Local Client\GeoGig Manager`` oder �ber das Symbol ``GeoGig Manager`` in der Toolbar.
Es �ffnet sich folgender Dialog:

 .. image:: images/geogig/GeoGigManagerDialog.png


Mit den beiden Pulldownmen�s in der ersten Zeile k�nnen Sie den Geogig Server sowie das gew�nschte Repository ausw�hlen. Diese m�ssen nat�rlich zuvor konfiguriert worden sein (vgl. ``Vorbereitung eines Repositiories``).

Die weiteren Kn�pfe der ersten Zeile haben folgende Funktionen:

| |BtnSync|       : Synchronisiert lokale �nderungen des aktuellen Branches und �nderungen auf dem Server.
| |BtnMergeDown|  : Merge �nderungen des �bergeordneten Branches zum aktuellen Branch
| |BtnMergeUp|    : Merge �nderungen des aktuellen Branches zum �bergeordneten Branch
| |BtnRevert|     : L�scht lokale �nderungen, die noch nicht zum Server gesandt wurden
| |BtnShowChanges|: Zeigt lokale �nderungen an, die noch nicht zum Server gesandt wurden

.. |BtnSync|        image:: images/geogig/BtnSync.PNG
.. |BtnMergeDown|   image:: images/geogig/BtnMergeDown.PNG
.. |BtnMergeUp|     image:: images/geogig/BtnMergeUp.PNG
.. |BtnRevert|      image:: images/geogig/BtnRevert.PNG
.. |BtnShowChanges| image:: images/geogig/BtnShowChanges.PNG


Unter der Knopfzeile befindet sich das Fenster mit dem Branch Tree. Die Wurzel aller Branches ist ``master``. Von hier k�nnen untergeordnete Branches hierarchisch angelegt werden. Der aktuelle Branch ist durch einen fette und etwas gr��ere Schrift hervorgehoben (im Snapshot oben ``B6``).
Durch einen Rechtsklick auf einen Branch erhalten Sie folgendes Popupmen�:

 .. image:: images/geogig/BranchesPulldown.PNG

Die Funktionen darin sind:

- **Goto this Branch**: Gehe mit allen Layern des Repositories zu diesem Branch und w�hle diesen als aktuellen Branch. Eine Progressbar oberhalb der Karte zeigt den Fortschritt dieser Aktion (f�r jeden ver�nderten Layer, geht es einen Schritt weiter). Der gew�hlte Branch wird danach fett und mit etwas gr��eren Buchstaben als aktueller Branch dargestellt. Merge- ind Synchronisationsaktionen beziehen sich nun auf diesen Branch.
- **Create branch**: Erzeugt einen Unterbranch zum gew�hlten Branch. Beachte: Man kann auch einen Unterbranch zu einem anderen Branch als dem aktuellen Branch erzeugen!
- **Delete branch**: L�sche den gew�hlten Branch. Beachte: Der gew�hlte Branch muss nicht der aktuelle Branch sein. Ein L�schen von ``master`` ist nicht m�glich. Besitzt ein Branch Unterbranches, so erfolgt eine zus�tzliche R�ckfrage an den Benutzer. Falls er zustimmt, wird der gew�hlte Branch und seine Unterbranches gel�scht.

Anmerkung zur Branchhierarchie:

	  In Geogig gibt es eigentlich keine Hierarchie unter den Branches. Alle Branches sind gleichberechtigt und daher kann der Benutzer auch von jedem Branch in jeden Branch mergen. Um die Bedienbarkeit des Plugins jedoch zu vereinfachen, haben wir hier eine Hierarchie eingef�gt. Technisch wird das �ber eine Namenskonvention erreicht: Der Wurzelbranch ist ``master``. Branches mit "einfachen" Namen sind master direkt untergeordnet. Ein Branch darunter hat den Namane seines �bergeordneten Branches mit folgender Notation im Namen eingebaut: "<eigener Name>_($<�bergeordneter Branch$)". Im Plugin wird nur der <eigene Name> angezeigt.

Unter dem Fenster mit dem Branchtree liegt das Fenster mit der Commithistorie. Wird im oberen Fenster ein Branch ausgew�hlt, so wird in diesem Fenster die Liste der Commits zu diesem Branch angezeigt. Durch einen Rechtsklick auf einen Commit erhalten Sie folgendes Pulldownmen�:

 .. image:: images/geogig/CommitsPulldown.PNG

Die Funktionen darin sind:

- **Create branch from this commit**: Erzeugt einen Unterbranch zum ausgew�hlten Branch basierend auf dem selektierten Commit.
- **Show changes of this commit**: �ffnet ein neues Men� mit allen �nderungen, die mit diesem Commit abgespeichert wurden.
- **Show details of this commit**: �ffnet ein neues Men� mit Informationen zu diesem Commit, u.a. Autor und Datum.
- **Create tag**: Erzeugt einen Tag zu diesem Commit
- **Delete tag**: L�scht alle Tags, die diesem Commit angeh�ngt waren.
	  




