/* Create Sequence for system_id */

CREATE SEQUENCE ga.system_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 138
  CACHE 1;
ALTER TABLE ga.system_id_seq
  OWNER TO postgres;
  
/* SET sequence to g_leitungsoeffnung */
ALTER TABLE IF EXISTS ga.g_leitungsoeffnung ALTER COLUMN IF EXISTS system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_kondensatsammelstelle */
ALTER TABLE IF EXISTS ga.g_kondensatsammelstelle ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_hausanschluss */
ALTER TABLE IF EXISTS ga.g_hausanschluss ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_abzweig */
ALTER TABLE IF EXISTS ga.g_abzweig ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_leitungsabschluss */
ALTER TABLE IF EXISTS ga.g_leitungsabschluss ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_absperrarmatur */
ALTER TABLE IF EXISTS ga.g_absperrarmatur ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_anschlussltg_abschnitt */
ALTER TABLE IF EXISTS ga.g_anschlussltg_abschnitt ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_versorgungsltg_abschnitt */
ALTER TABLE IF EXISTS ga.g_versorgungsltg_abschnitt ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_hauptltg_abschnitt */
ALTER TABLE IF EXISTS ga.g_hauptltg_abschnitt ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_schacht */
ALTER TABLE IF EXISTS ga.g_schacht ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_regelstation */
ALTER TABLE IF EXISTS ga.g_regelstation ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_schutzmassnahme */
ALTER TABLE IF EXISTS ga.g_schutzmassnahme ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);

/* SET sequence to g_anlage_station */
ALTER TABLE IF EXISTS ga.g_anlage_station ALTER COLUMN system_id SET DEFAULT nextval(('ga.system_id_seq'::text)::regclass);