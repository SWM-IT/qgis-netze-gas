/* Tabelle g_uebergang*/
ALTER TABLE IF EXISTS ga.g_uebergang 
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_vo CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_vorp CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_still CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_voruebergehend CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_plan CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_ausgeba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_voruebe CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_stillge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_betr CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_im_ba CASCADE;



/* Tabelle g_hauptltg_nummer*/
ALTER TABLE IF EXISTS ga.g_hauptltg_nummer  
  DROP COLUMN IF EXISTS nummer_in_planung CASCADE,  
  DROP COLUMN IF EXISTS nummer_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS nummer_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS nummer_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS nummer_im_bau CASCADE,  
  DROP COLUMN IF EXISTS nummer_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS nummer_in_betrieb CASCADE;



/* Tabelle g_anlage_station*/
ALTER TABLE IF EXISTS ga.g_anlage_station  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE;



/* Tabelle g_knickpunkt*/
ALTER TABLE IF EXISTS ga.g_knickpunkt  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_stillge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_vorp CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_voruebe CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_plan CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_im_ba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_betr CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_ausgeba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_vo CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_still CASCADE;



/* Tabelle g_hochdruckleitung_lt_st*/
ALTER TABLE IF EXISTS ga.g_hochdruckleitung_lt_st  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE;



/* Tabelle g_ueberdeckung*/
ALTER TABLE IF EXISTS ga.g_ueberdeckung  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE;



/* Tabelle g_uebersichtfort*/
ALTER TABLE IF EXISTS ga.g_uebersichtfort  
  DROP COLUMN IF EXISTS text_es_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_s_nummer CASCADE,  
  DROP COLUMN IF EXISTS text CASCADE,  
  DROP COLUMN IF EXISTS text_fm_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_mk_nummer CASCADE,  
  DROP COLUMN IF EXISTS zusatzbeschriftung CASCADE,  
  DROP COLUMN IF EXISTS text_nenndurchmesser CASCADE,  
  DROP COLUMN IF EXISTS text_gemeindename CASCADE,  
  DROP COLUMN IF EXISTS text_noteinspeisung CASCADE,  
  DROP COLUMN IF EXISTS text_generalumgang CASCADE,  
  DROP COLUMN IF EXISTS text_ueberspeiseregelanl CASCADE,  
  DROP COLUMN IF EXISTS text_fsa CASCADE,  
  DROP COLUMN IF EXISTS text_odorieranlage CASCADE,  
  DROP COLUMN IF EXISTS text_h_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_kh_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_hochdruckbezeichnung CASCADE,  
  DROP COLUMN IF EXISTS text_unset CASCADE,  
  DROP COLUMN IF EXISTS text_k_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_kompensator CASCADE,  
  DROP COLUMN IF EXISTS text_ab_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_katasternummer CASCADE,  
  DROP COLUMN IF EXISTS text_ks_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_sonde CASCADE,  
  DROP COLUMN IF EXISTS text_leitungseigentum CASCADE,  
  DROP COLUMN IF EXISTS text_allgem_beschriftung CASCADE,  
  DROP COLUMN IF EXISTS text_absperrbezirk CASCADE,  
  DROP COLUMN IF EXISTS text_uebergabe_uebernahmestation CASCADE,  
  DROP COLUMN IF EXISTS text_lor_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_bezirksschieber CASCADE,  
  DROP COLUMN IF EXISTS text_mantelrohr CASCADE,  
  DROP COLUMN IF EXISTS text_e_nummer CASCADE,  
  DROP COLUMN IF EXISTS text_reglerbeschriftung CASCADE;

/* Tabelle g_absperrarmatur*/
ALTER TABLE IF EXISTS ga.g_absperrarmatur  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_vo CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_in_vo CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_voruebe CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_still CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_vorp CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_im_ba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_plan CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_ausgeba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_betr CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_im_ba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_stillge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_still CASCADE;



/* Tabelle g_hauptltg_abschnitt*/
ALTER TABLE IF EXISTS ga.g_hauptltg_abschnitt  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_in_vo CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_im_ba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_uebersicht_still CASCADE;



/* Tabelle g_schutzbereich_netzteil*/
ALTER TABLE IF EXISTS ga.g_schutzbereich_netzteil  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE;



/* Tabelle g_zustaendigkeitsbereich_beschr*/
ALTER TABLE IF EXISTS ga.g_zustaendigkeitsbereich_beschr  
  DROP COLUMN IF EXISTS text_planungsbereich CASCADE,  
  DROP COLUMN IF EXISTS text_wartungsbereich CASCADE,  
  DROP COLUMN IF EXISTS text_betriebsbereich CASCADE,  
  DROP COLUMN IF EXISTS text_absperrbezirk CASCADE;



/* Tabelle g_hauptltg_name*/
ALTER TABLE IF EXISTS ga.g_hauptltg_name  
  DROP COLUMN IF EXISTS name_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS name_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS name_in_planung CASCADE,  
  DROP COLUMN IF EXISTS name_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS name_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS name_im_bau CASCADE,  
  DROP COLUMN IF EXISTS name_ausgebaut CASCADE;



/* Tabelle g_leitungsabschluss*/
ALTER TABLE IF EXISTS ga.g_leitungsabschluss  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_plan CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_ausgeba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_still CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_vorp CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_stillge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_betr CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_im_ba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_voruebe CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_vo CASCADE;



/* Tabelle g_markierung*/
ALTER TABLE IF EXISTS ga.g_markierung  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE;



/* Tabelle g_aufnahmepunkt*/
ALTER TABLE IF EXISTS ga.g_aufnahmepunkt  
  DROP COLUMN IF EXISTS nummer_code CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehe CASCADE,  
  DROP COLUMN IF EXISTS code CASCADE;



/* Tabelle g_detailzeichnung*/
ALTER TABLE IF EXISTS ga.g_detailzeichnung  
  DROP COLUMN IF EXISTS beschriftung CASCADE;



/* Tabelle g_erfassungsgebiet*/
ALTER TABLE IF EXISTS ga.g_erfassungsgebiet  
  DROP COLUMN IF EXISTS beschriftung CASCADE;



/* Tabelle g_kondensatsammelstelle*/
ALTER TABLE IF EXISTS ga.g_kondensatsammelstelle  
  DROP COLUMN IF EXISTS beschriftung_nummer_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_nummer_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_nummer_voruebergeh CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_vo CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_voruebe CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_still CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_nummer_in_vorplanu CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_nummer_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_vorp CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_plan CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_ausgeba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_nummer_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_nummer_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_betr CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_im_ba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_stillge CASCADE;



/* Tabelle g_zustaendigkeitsbereich*/
ALTER TABLE IF EXISTS ga.g_zustaendigkeitsbereich  
  DROP COLUMN IF EXISTS beschriftung_wartungsbereich CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_planungsbereich CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_betriebsbereich CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_absperrbezirk CASCADE;



/* Tabelle g_messpunkt*/
ALTER TABLE IF EXISTS ga.g_messpunkt  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE;



/* Tabelle g_leitungsoeffnung*/
ALTER TABLE IF EXISTS ga.g_leitungsoeffnung  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_vo CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_voruebe CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_ausgeba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_still CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_im_ba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_betr CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_plan CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_vorp CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_stillge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE;



/* Tabelle g_regelstation*/
ALTER TABLE IF EXISTS ga.g_regelstation  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE;



/* Tabelle g_hochdruckleitung*/
ALTER TABLE IF EXISTS ga.g_hochdruckleitung  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE;



/* Tabelle g_versorgungsltg_baujahr_beschr*/
ALTER TABLE IF EXISTS ga.g_versorgungsltg_baujahr_beschr  
  DROP COLUMN IF EXISTS baujahr_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS baujahr_im_bau CASCADE,  
  DROP COLUMN IF EXISTS baujahr_in_planung CASCADE,  
  DROP COLUMN IF EXISTS baujahr_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS baujahr_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS baujahr_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS baujahr_voruebergehend_a_b CASCADE;



/* Tabelle g_schutzbereich*/
ALTER TABLE IF EXISTS ga.g_schutzbereich  
  DROP COLUMN IF EXISTS beschriftung_name_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_name_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_name_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_name_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_name_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_name_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_voruebergehend_a_b CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_name_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_name CASCADE;



/* Tabelle g_fehlertext*/
ALTER TABLE IF EXISTS ga.g_fehlertext  
  DROP COLUMN IF EXISTS textgeometrie CASCADE;



/* Tabelle g_abzweig*/
ALTER TABLE IF EXISTS ga.g_abzweig  
  DROP COLUMN IF EXISTS beschr_gswaechter_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter2_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter2_voruebergehend CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_voruebe CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter2_in_planung CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_ausgebaut CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_vorue CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_im_ba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_ausgeba CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_betr CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_plan CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter2_in_betrieb CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter2_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_voruebergehend CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_ausge CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_stillge CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter_in_vorplanung CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_vo CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_in_vorp CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter2 CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_still CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_hoehenwert_im_bau CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter2_stillgelegt CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_pl CASCADE,  
  DROP COLUMN IF EXISTS beschriftung_ueberdeckung_in_be CASCADE,  
  DROP COLUMN IF EXISTS beschr_gswaechter2_ausgebaut CASCADE;

