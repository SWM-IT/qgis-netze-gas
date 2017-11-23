-- 
-- Test to create some simple tables for tests with GeoGig
--

-- I copy the table ga.g_hauptltg_abschnitt with various 
-- combinations of fields, so that I get tables where I
-- can test various field types.

----------------------------------------------------
-- Test field type boolean
--
DROP TABLE IF EXISTS ga.test_bool;

CREATE TABLE ga.test_bool
(
  system_id bigint NOT NULL,
  material character varying(15),
  bezugslinie_darstellen_ boolean,
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_bool
  OWNER TO admin;

CREATE INDEX sp_test_bool_d_leitung_in_betrieb
  ON ga.test_bool
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_bool 
  (system_id, 
   material,
   bezugslinie_darstellen_,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   bezugslinie_darstellen_,
   d_leitung_in_betrieb 
  FROM ga.g_hauptltg_abschnitt;

----------------------------------------------------
-- Test field type bigint
--
DROP TABLE IF EXISTS ga.test_bigint;

CREATE TABLE ga.test_bigint
(
  system_id bigint NOT NULL,
  material character varying(15),
  unterstammnummer bigint,
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_bigint
  OWNER TO admin;

CREATE INDEX sp_test_bigint_d_leitung_in_betrieb
  ON ga.test_bigint
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_bigint 
  (system_id, 
   material,
   unterstammnummer,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   unterstammnummer,
   d_leitung_in_betrieb 
  FROM ga.g_hauptltg_abschnitt;

----------------------------------------------------
-- Test field type date
--
DROP TABLE IF EXISTS ga.test_date;

CREATE TABLE ga.test_date
(
  system_id bigint NOT NULL,
  material character varying(15),
  datum_letzte_statusaenderung date,
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_date
  OWNER TO admin;

CREATE INDEX sp_test_date_d_leitung_in_betrieb
  ON ga.test_date
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_date 
  (system_id, 
   material,
   datum_letzte_statusaenderung,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   datum_letzte_statusaenderung,
   d_leitung_in_betrieb 
  FROM ga.g_hauptltg_abschnitt;

----------------------------------------------------
-- Test field type real
--
DROP TABLE IF EXISTS ga.test_real;

CREATE TABLE ga.test_real
(
  system_id bigint NOT NULL,
  material character varying(15),
  laenge_gis real,
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_real
  OWNER TO admin;

CREATE INDEX sp_test_real_d_leitung_in_betrieb
  ON ga.test_real
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_real 
  (system_id, 
   material,
   laenge_gis,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   laenge_gis,
   d_leitung_in_betrieb 
  FROM ga.g_hauptltg_abschnitt;

----------------------------------------------------
-- Test field type text
--
DROP TABLE IF EXISTS ga.test_text;

CREATE TABLE ga.test_text
(
  system_id bigint NOT NULL,
  material character varying(15),
  bemerkungen text,
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_text
  OWNER TO admin;

CREATE INDEX sp_test_text_d_leitung_in_betrieb
  ON ga.test_text
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_text 
  (system_id, 
   material,
   bemerkungen,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   bemerkungen,
   d_leitung_in_betrieb 
  FROM ga.g_hauptltg_abschnitt;

----------------------------------------------------
-- Test field type numeric
--
DROP TABLE IF EXISTS ga.test_numeric;

CREATE TABLE ga.test_numeric
(
  system_id bigint NOT NULL,
  material character varying(15),
  beschriftung_uebersicht_in_be_just_x numeric,
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_numeric
  OWNER TO admin;

CREATE INDEX sp_test_numeric_d_leitung_in_betrieb
  ON ga.test_numeric
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_numeric 
  (system_id, 
   material,
   beschriftung_uebersicht_in_be_just_x,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   beschriftung_uebersicht_in_be_just_x,
   d_leitung_in_betrieb 
  FROM ga.g_hauptltg_abschnitt;

----------------------------------------------------
-- Test field type bigint_vec
--
DROP TABLE IF EXISTS ga.test_bigint_vec;

CREATE TABLE ga.test_bigint_vec
(
  system_id bigint NOT NULL,
  material character varying(15),
  rwo_id bigint[],
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_bigint_vec
  OWNER TO admin;

CREATE INDEX sp_test_bigint_vec_d_leitung_in_betrieb
  ON ga.test_bigint_vec
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_bigint_vec 
  (system_id, 
   material,
   rwo_id,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   rwo_id,
   d_leitung_in_betrieb 
  FROM ga.g_hauptltg_abschnitt;


----------------------------------------------------
-- Test field type timestamp
--
DROP TABLE IF EXISTS ga.test_timestamp;

CREATE TABLE ga.test_timestamp
(
  system_id bigint NOT NULL,
  material character varying(15),
  sw_exported_on timestamp without time zone,
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_timestamp
  OWNER TO admin;

CREATE INDEX sp_test_timestamp_d_leitung_in_betrieb
  ON ga.test_timestamp
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_timestamp 
  (system_id, 
   material,
   sw_exported_on,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   sw_exported_on,
   d_leitung_in_betrieb 
  FROM ga.g_hauptltg_abschnitt;

----------------------------------------------------
-- Test field type uuid
--

DROP TABLE IF EXISTS ga.test_uuid;

CREATE TABLE ga.test_uuid
(
  system_id bigint NOT NULL,
  material character varying(15),
  uuid uuid DEFAULT uuid_generate_v1(),
  d_leitung_in_betrieb geometry(LineString,31468)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE ga.test_uuid
  OWNER TO admin;

CREATE INDEX sp_test_uuid_d_leitung_in_betrieb
  ON ga.test_uuid
  USING gist
  (d_leitung_in_betrieb);

INSERT INTO ga.test_uuid 
  (system_id, 
   material,
   uuid,
   d_leitung_in_betrieb) 
  SELECT 
   system_id, 
   material,
   uuid,
   d_leitung_in_betrieb 
  FROM ga.g_versorgungsltg_abschnitt;