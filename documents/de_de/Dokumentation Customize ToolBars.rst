============================================
*GUI anpassen mit Customize ToolBars Plugin*
============================================

:Autor: Jan Gerste
:Date: $Date: 2017-10-05 12:40:42 +0000 (Thu, 05 Oct 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Erstellung eigener Toolbars mit Hilfe des **Customize ToolBars** Plugins.


Installation
------------

Laden Sie das Plugin **Customize Toolbars** über Ihr QGIS unter **Erweiterungen => Erweiterungen verwalten und installieren** herunter und aktivieren Sie dieses anschließend. Nach erfolgreicher Installation finden Sie im Menü **"Erweiterungen"** den Eintrag **Customize ToolBars => Customize ToolBars** über den Sie das Konfigurationsfenster öffnen können.


Erstellen und editieren von Toolbars
------------------------------------

Zum Erstellen einer neuen Toolbar klicken Sie im Konfigurationsfenster auf die Schaltfläche **"New ToolBar"**. In dem öffnenden Fenster geben Sie einen Namen für die neue Toolbar ein und klicken **OK**. Nun sehen Sie im rechten Feld einen neuen Eintrag mit dem Namen Ihrer Toolbar. Der Name lässt sich nachträglich über die Schaltfläche **"Rename ToolBar"** ändern.

Um der Toolbar Icons zuzuordnen wählen Sie diese aus den bereits existierenden Toolbars und Menüs aus (linke Seite ) und ziehen sie diese per Drag&Drop in Ihre neue Toolbar hinein. Dabei ist darauf zu achten, dass diese Icons nur innerhalb einer Toolbar, d.h. nicht auf der freien weißen Fläche in der rechten Spalte, abgelegt werden können. Ein gültiger Ablagepunkt wird durch einen schwarzen Rahmen um ein Element oder einer Linie zwischen zwei Elementen dargestellt. Ebenso können Sie die Position der einzelnen Icons durch Ziehen ändern.

Um Icons aus einer Toolbar zu entfernen oder ganze Toolbars zu löschen, wählen Sie das entsprechende Element aus und klicken anschließend auf die Schaltfläche **"Delete ToolBar or Tool"**.

Abschießend klicken Sie die Schaltfläche **"Save Changes"** an, um Ihre Toolbars zu speichern. Diese können nun wie gewohnt über das Menü **Ansicht => Werkzeugkästen** oder einen Rechtsklick auf die freie Fläche auf Menü- oder Werkzeugleisten aktiviert und deaktiviert werden. Durch Drag&Drop können sie beliebig im QGIS Fenster platziert werden.

Die erstellten bzw. angepassten Toolbars werden im **Benutzerverzeichnis** menstens unter *C:/Users/BENUTZERNAME* in der Datei **".CustomToolBars"** gespeichert. Diese Datei kann dazu genutzt werden das alle Nutzer die gleichen Toolbars im QGis verwenden, indem Sie in die jeweiligen Benutzerverzeichnisse kopiert wird.