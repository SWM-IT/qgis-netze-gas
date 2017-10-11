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

Per SQL-Befehl können dann die Topologie-Tabellen über eine bereitgestellte Funktion in einem neuen Schema erzeugt werden. Im Beispiel im **Schema** 'gas_topo' mit der **SRID** 31468:

 **SELECT topology.CreateTopology('gas_topo', 31468)**

Die neue Topologie wird in der Datenbank unter dem Schema topology in die Tabelle topology eingetragen.

Anschließend werden die GIS Topologie Daten in neuen Tabellen kopiert:

 **INSERT INTO gas_topo.node SELECT node_id[3], 0, ST_SETSRID(ST_MakePoint(coord[1] * 0.001, coord[2] * 0.001),31468) from ga.sw_gis_node;**

 **INSERT INTO gas_topo.edge_data SELECT link_id[3], first_node_id[3], last_node_id[3], link_id[3], link_id[3], link_id[3], link_id[3], 0, 0, ST_SETSRID(ST_MakeLine(ST_MakePoint(coord_1[1] * 0.001, coord_1[2] * 0.001), ST_MakePoint(coord_2[1] * 0.001, coord_2[2] * 0.001)),31468) from ga.sw_gis_link;**

Jetzt können für alle Tabellen mit Geometrien die TopoGeometry Spalte hinzugefügt und gefüllt werden.
Im Besipiel für Hausanschluss und Anschlussleitung:

    **SELECT AddTopoGeometryColumn('gas_topo', 'ga', 'g_anschlussltg_abschnitt', 'g', 'LINE');**

    **UPDATE ga.g_anschlussltg_abschnitt t SET g = CreateTopoGeom('gas_topo',2, 1,CAST('{{' || (SELECT link_id[3] FROM ga.sw_gis_chain_link where chain_id = (SELECT chain_id FROM ga.sw_gis_chain WHERE rwo_id = t.rwo_id LIMIT 1) LIMIT 1) || ',2}}' AS integer[]));**
    
    **SELECT AddTopoGeometryColumn('gas_topo', 'ga', 'g_hausanschluss', 'g', 'POINT');**

    **UPDATE ga.g_hausanschluss t SET g = CreateTopoGeom('gas_topo',1,2,CAST('{{' || (SELECT node_id[3] FROM ga.sw_gis_point where rwo_id = t.rwo_id OFFSET 0 LIMIT 1) || ',1}}' AS integer[])) WHERE system_id IN (SELECT system_id FROM ga.g_hausanschluss t WHERE (SELECT node_id[3] FROM ga.sw_gis_point where rwo_id = t.rwo_id OFFSET 0 LIMIT 1) IS NOT NULL);**


    