================================================
*Installation des TopologicGeometryEdit Plugins*
================================================

:Autor: Holger Fischer
:Date: $Date: 2017-10-11 13:20:23 +0000 (Wed, 11 Oct 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Die notwendigen Schritte zur Einrichtung des TopologicGeometryEdit Plugins.

Vorbereitung der PostgreSQL Datenbank
-------------------------------------
Um Topologie in QGIS nutzbar zu machen, müssen folgende **Datenbankerweiterungen** installiert werden:
 - postgis
 - postgis_topology

Diese können im Kontextmenu der Datenbank hinzugefügt werden:
 .. image:: images/topology_extensions.png

Per `SQL-Skript <../../source/SQL/Script_create_topology_entries.sql>`_ können dann die Topologie-Tabellen über eine bereitgestellte Funktion in einem neuen Schema erzeugt und gefüllt werden.

Hinzufügen der Topologie-Layer im QGis
--------------------------------------

Für die Topologie Funktion müssen 2 Postgis Layer ergänzt werden.
In der Menüzeile über 'Layer > Layer hinzufügen > PostGis Layer' nach Auswahl der Datenbank und verbinden, die Layer 'edge_data' und 'node' hinzufügen. Anschließend muss noch der Layer 'edge_data' in 'edge' umbenannt werden.
