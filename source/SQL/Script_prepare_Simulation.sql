
-- Add a topogeom column
SELECT AddTopoGeometryColumn('gas_topo', 'ga', 'g_absperrarmatur', 'g', 'POINT');

-- Update the column with 
UPDATE ga.g_absperrarmatur t SET g = CreateTopoGeom('gas_topo',1,5,CAST ('{{' || (SELECT k.node_id[3]) || ',1}}' AS integer[])) FROM ga.sw_gis_point k where k.rwo_id = t.rwo_id and k.app_code = 1;
UPDATE ga.g_absperrarmatur t SET g = CreateTopoGeom('gas_topo',1,5,CAST ('{{' || (SELECT k.node_id[3]) || ',1}}' AS integer[])) FROM ga.sw_gis_point k where k.rwo_id = t.rwo_id and k.app_code = 6;
UPDATE ga.g_absperrarmatur t SET g = CreateTopoGeom('gas_topo',1,5,CAST ('{{' || (SELECT k.node_id[3]) || ',1}}' AS integer[])) FROM ga.sw_gis_point k where k.rwo_id = t.rwo_id and k.app_code = 7;

-- Add missing system_id to the absperrarmatur table
ALTER TABLE ga.g_absperrarmatur ADD COLUMN system_id INTEGER;
CREATE SEQUENCE ga.test_id_seq OWNED by ga.g_absperrarmatur.system_id;
ALTER TABLE ga.g_absperrarmatur ALTER COLUMN system_id SET DEFAULT nextval('ga.test_id_seq');
UPDATE ga.g_absperrarmatur SET system_id = nextval('ga.test_id_seq');

-- OPTIONAL --

INSERT INTO ga.g_absperrarmatur (g,armaturenstellung) VALUES(CreateTopoGeom('gas_topo',1,5,'{{437082429,1}}'),'geschlossen');
INSERT INTO ga.g_absperrarmatur (g,armaturenstellung) VALUES(CreateTopoGeom('gas_topo',1,5,'{{11865607,1}}'),'geschlossen');

-- For Insert --

/* SET sequence to g_absperrarmatur */
ALTER TABLE IF EXISTS ga.g_absperrarmatur ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* Functions */
CREATE OR REPLACE FUNCTION topology.simulate(startnodes character varying,topology text,scheme text,tablename character varying,attribute character varying,criterium character varying)
RETURNS TABLE (
edge_id integer,
start_node integer,
end_node integer
) AS
$func$
DECLARE
	SQL text;
BEGIN

	SQL = 'WITH RECURSIVE path AS (
	SELECT edge_id, start_node, end_node
	FROM ' || topology ||'.edge_data
	WHERE start_node = ANY (''{'|| startnodes || '}''::int[]) OR end_node = ANY (''{'|| startnodes || '}''::int[])
	UNION
	SELECT e.edge_id, e.start_node, e.end_node
	FROM ' || topology ||'.edge_data e, path s
	WHERE (s.start_node = e.start_node OR s.start_node = e.end_node OR s.end_node = e.end_node OR s.end_node = e.start_node)
	AND (SELECT * FROM topology.validateCombined(''' || topology || ''','''|| scheme ||''','''|| tablename ||''','''|| attribute ||''','''|| criterium ||''',e.start_node,1)) = false
	AND (SELECT * FROM topology.validateCombined(''' || topology || ''','''|| scheme ||''','''|| tablename ||''','''|| attribute ||''','''|| criterium ||''',e.end_node,1)) = false) 
	SELECT DISTINCT e.edge_id, e.start_node, e.end_node
	FROM path s, ' || topology ||'.edge_data e
	WHERE e.edge_id = s.edge_id
	OR e.start_node = s.end_node
	OR e.end_node = s.start_node
	OR e.start_node = s.start_node
	OR e.end_node = s.end_node;';
	
	RETURN QUERY EXECUTE SQL;
END
$func$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION topology.validateCombined(topology text,scheme text,tablename character varying,attribute character varying,criterium character varying,elementid int,typeid int)
RETURNS boolean
AS
$func$
DECLARE
	SQL text;
	validation boolean;
	SQL2 text;
	SQL_DYNAMIC text = 'SELECT r.topogeo_id,l.table_name,l.feature_column FROM '|| topology||'.relation r,topology.layer l WHERE l.table_name = ''' || tablename ||''' and r.element_id = '|| elementid ||' and r.element_type = '|| typeid ||' and l.layer_id = r.layer_id and l.schema_name = '''|| scheme ||'''';
	my_record RECORD;
BEGIN

	 CREATE TEMPORARY TABLE IF NOT EXISTS temp_
	(
	id int,
	s_name character varying,
	t_name character varying
	) ON COMMIT DELETE ROWS;

	TRUNCATE temp_;
	
	FOR my_record IN EXECUTE SQL_DYNAMIC
	LOOP 
		SQL = 'INSERT INTO temp_ VALUES((SELECT system_id FROM ' || scheme || '.' || my_record.table_name || ' WHERE id(' || my_record.feature_column ||' ) = ' || my_record.topogeo_id || '),''' ||  scheme || ''',''' ||  my_record.table_name || ''')';
		EXECUTE SQL;
	END LOOP;   
	
	SQL2 = 'SELECT ((SELECT ' || attribute || ' FROM ' || scheme || '.' || tablename || ' WHERE system_id = (SELECT id FROM temp_ WHERE t_name = ''' || tablename || ''')) = ''' || criterium || ''');';
	EXECUTE SQL2 into validation;

	IF(validation IS NOT TRUE)THEN
		return false;
	END IF;
		
	return validation as validation;
END
$func$ LANGUAGE plpgsql;
