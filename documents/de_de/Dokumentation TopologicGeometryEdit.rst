================================================
*Installation des TopologicGeometryEdit Plugins*
================================================

:Autor: Holger Fischer
:Date: $Date: 2017-10-11 13:20:23 +0000 (Wed, 11 Oct 2017) $
:Version: $Revision: 1.0 $
:Beschreibung: Die notwendigen Schritte zur Einrichtung des TopologicGeometryEdit Plugins.

Vorbereitung der PostgreSQL Datenbank
-------------------------------------
Um Topologie in QGIS nutzbar zu machen, m�ssen folgende **Datenbankerweiterungen** installiert werden:
 - postgis
 - postgis_topology

Diese k�nnen im Kontextmenu der Datenbank hinzugef�gt werden:
 .. image:: images/topology_extensions.png

Per `SQL-Skript <../../source/SQL/Script_create_topology_entries.sql>`_ k�nnen dann die Topologie-Tabellen �ber eine bereitgestellte Funktion in einem neuen Schema erzeugt und gef�llt werden. Au�erdem wird eine Sequenz auf der Spalte 'system_id' der verwendeten Tabellen erstellt um das Einf�gen neuer Objekte zu erm�glichen.

Hinzuf�gen der Topologie-Layer im QGis
--------------------------------------
F�r die Topologie Funktion m�ssen 2 Postgis Layer erg�nzt werden.
In der Men�zeile �ber 'Layer > Layer hinzuf�gen > PostGis Layer' nach Auswahl der Datenbank und verbinden, die Layer 'edge_data' und 'node' hinzuf�gen. Anschlie�end muss noch der Layer 'edge_data' in 'edge' umbenannt werden.

Hinzuf�gen der Topologie-Plugins im QGis
----------------------------------------
Aktuell sind die Topologie-Funktionen auf zwei Plugins verteilt:
 - Topologic Geometry Add
 - Topologic Geometry Edit

Beide Plugins k�nnen �ber das Men� **Erweiterungen|Erweiterungen hinzuf�gen und installieren** nachdem die Sourcen im Plugin-Verzeichnis abgelegt wurden hinzugef�gt werden.