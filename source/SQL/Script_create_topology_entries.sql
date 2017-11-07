/* Create topology entries */

/* create topology tables */
--SELECT DropTopology('gas_topo');
SELECT topology.CreateTopology('gas_topo', 31468);

/* copy data from sw_gis_node to node table */
INSERT INTO gas_topo.node SELECT node_id[3], 0, ST_SETSRID(ST_MakePoint(coord[1] * 0.001, coord[2] * 0.001),31468) from ga.sw_gis_node;

/* copy data from sw_gis_link to edge table */
INSERT INTO gas_topo.edge_data SELECT link_id[3], first_node_id[3], last_node_id[3], link_id[3], link_id[3], link_id[3], link_id[3], 0, 0, ST_SETSRID(ST_MakeLine(ST_MakePoint(coord_1[1] * 0.001, coord_1[2] * 0.001), ST_MakePoint(coord_2[1] * 0.001, coord_2[2] * 0.001)),31468) from ga.sw_gis_link;

/* create topology column for g_anschlussltg_abschnitt */
SELECT AddTopoGeometryColumn('gas_topo', 'ga', 'g_anschlussltg_abschnitt', 'g', 'LINE');

/* fill topology column of g_anschlussltg_abschnitt */
UPDATE ga.g_anschlussltg_abschnitt t SET g = CreateTopoGeom('gas_topo',2, 1,CAST(array (SELECT CAST ('{' || k.link_id[3] || ',2}' AS integer[]) FROM ga.sw_gis_chain_link k, ga.sw_gis_chain h where k.chain_id = h.chain_id and h.rwo_id = t.rwo_id ) AS integer[]));

/* create topology column for g_hausanschluss */
SELECT AddTopoGeometryColumn('gas_topo', 'ga', 'g_hausanschluss', 'g', 'POINT');

/* fill topology column of g_hausanschluss */
UPDATE ga.g_hausanschluss t SET g = CreateTopoGeom('gas_topo',1,2,CAST('{{' || (SELECT node_id[3] FROM ga.sw_gis_point where rwo_id = t.rwo_id OFFSET 0 LIMIT 1) || ',1}}' AS integer[])) WHERE system_id IN (SELECT system_id FROM ga.g_hausanschluss t WHERE (SELECT node_id[3] FROM ga.sw_gis_point where rwo_id = t.rwo_id OFFSET 0 LIMIT 1) IS NOT NULL);

/* create topology column for g_abzweig */
SELECT AddTopoGeometryColumn('gas_topo', 'ga', 'g_abzweig', 'g', 'POINT');

/* fill topology column of g_abzweig */
/*UPDATE ga.g_abzweig t SET g = CreateTopoGeom('gas_topo',1,3,CAST('{{' || (SELECT node_id[3] FROM ga.sw_gis_point where rwo_id = t.rwo_id OFFSET 0 LIMIT 1) || ',1}}' AS integer[])) WHERE system_id IN (SELECT system_id FROM ga.g_abzweig t WHERE (SELECT node_id[3] FROM ga.sw_gis_point where rwo_id = t.rwo_id OFFSET 0 LIMIT 1) IS NOT NULL);*/
/*UPDATE ga.g_abzweig t SET g = CreateTopoGeom('gas_topo',1,3,CAST(array (SELECT CAST ('{' || k.node_id[3] || ',1}' AS integer[]) FROM ga.sw_gis_point k,ga.g_abzweig t where k.rwo_id = t.rwo_id AND k.app_code = 15 LIMIT 1) AS integer[]));*/
UPDATE ga.g_abzweig t SET g = CreateTopoGeom('gas_topo',1,3,CAST ('{{' || (SELECT k.node_id[3]) || ',1}}' AS integer[])) FROM ga.sw_gis_point k where k.rwo_id = t.rwo_id and k.app_code = 15;

/* create topology column for g_versorgungsltg_abschnitt */
SELECT AddTopoGeometryColumn('gas_topo', 'ga', 'g_versorgungsltg_abschnitt', 'g', 'LINE');

/* fill topology column of g_versorgungsltg_abschnitt */
UPDATE ga.g_versorgungsltg_abschnitt t SET g = CreateTopoGeom('gas_topo',2, 4,CAST(array (SELECT CAST ('{' || k.link_id[3] || ',2}' AS integer[]) FROM ga.sw_gis_chain_link k, ga.sw_gis_chain h where k.chain_id = h.chain_id and h.rwo_id = t.rwo_id )AS integer[]));

