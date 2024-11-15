CREATE SCHEMA IF NOT EXISTS la_crimes;

CREATE TABLE IF NOT EXISTS la_crimes.area (
  area_id INTEGER NOT NULL,
  area_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (area_id)
);

CREATE TABLE IF NOT EXISTS la_crimes.crime_chronicle (
  date_occ DATE NOT NULL,
  time_occ TIME NOT NULL,
  PRIMARY KEY (date_occ, time_occ)
);

CREATE TABLE IF NOT EXISTS la_crimes.crime_location (
  location VARCHAR(100) NOT NULL,
  lat NUMERIC(10,7) NOT NULL,
  lon NUMERIC(10,7) NOT NULL,
  cross_street VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (location)
);

CREATE TABLE IF NOT EXISTS la_crimes.status (
  status VARCHAR(10) NOT NULL,
  status_desc VARCHAR(100) NOT NULL,
  PRIMARY KEY (status)
);

CREATE TABLE IF NOT EXISTS la_crimes.premises (
  premis_cd INTEGER NOT NULL,
  premis_desc VARCHAR(100) NOT NULL,
  PRIMARY KEY (premis_cd)
);

CREATE TABLE IF NOT EXISTS la_crimes.reporting_district (
  rpt_dist_no INTEGER NOT NULL,
  area_area_id INTEGER NOT NULL,
  PRIMARY KEY (rpt_dist_no),
  FOREIGN KEY (area_area_id)
    REFERENCES la_crimes.area (area_id)
);

CREATE TABLE IF NOT EXISTS la_crimes.crime_type (
  crm_cd INTEGER NOT NULL,
  crm_cd_desc VARCHAR(100) NOT NULL,
  crm_cd_2 INTEGER NOT NULL DEFAULT -1,
  crm_cd_3 INTEGER NOT NULL DEFAULT -1,
  crm_cd_4 INTEGER NOT NULL DEFAULT -1,
  PRIMARY KEY (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4)
);

CREATE TABLE IF NOT EXISTS la_crimes.crime_report (
  dr_no INTEGER NOT NULL,
  date_rptd DATE NOT NULL,
  crime_chronicle_date_occ DATE NOT NULL,
  crime_chronicle_time_occ TIME NOT NULL,
  status_status VARCHAR(10) NOT NULL,
  premises_premis_cd INTEGER NOT NULL,
  reporting_district_rpt_dist_no INTEGER NOT NULL,
  area_area_id INTEGER NOT NULL,
  crime_location_location VARCHAR(100) NOT NULL,
  mocodes VARCHAR(50),
  crime_type_crm_cd INTEGER NOT NULL,
  crime_type_crm_cd_2 INTEGER NOT NULL DEFAULT -1,
  crime_type_crm_cd_3 INTEGER NOT NULL DEFAULT -1,
  crime_type_crm_cd_4 INTEGER NOT NULL DEFAULT -1,
  PRIMARY KEY (dr_no),
  FOREIGN KEY (status_status) REFERENCES la_crimes.status (status),
  FOREIGN KEY (premises_premis_cd) REFERENCES la_crimes.premises (premis_cd),
  FOREIGN KEY (reporting_district_rpt_dist_no) REFERENCES la_crimes.reporting_district (rpt_dist_no),
  FOREIGN KEY (area_area_id) REFERENCES la_crimes.area (area_id),
  FOREIGN KEY (crime_location_location) REFERENCES la_crimes.crime_location (location),
  FOREIGN KEY (crime_chronicle_date_occ, crime_chronicle_time_occ) REFERENCES la_crimes.crime_chronicle (date_occ, time_occ),
  FOREIGN KEY (crime_type_crm_cd, crime_type_crm_cd_2, crime_type_crm_cd_3, crime_type_crm_cd_4) REFERENCES la_crimes.crime_type (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4)
);

CREATE TABLE IF NOT EXISTS la_crimes.weapon (
  weapon_used_cd INTEGER NOT NULL,
  weapon_desc VARCHAR(100) NOT NULL,
  PRIMARY KEY (weapon_used_cd)
);

CREATE TABLE IF NOT EXISTS la_crimes.crime_report_has_weapon (
  crime_report_dr_no INTEGER NOT NULL,
  weapon_weapon_used_cd INTEGER NOT NULL,
  PRIMARY KEY (crime_report_dr_no, weapon_weapon_used_cd),
  FOREIGN KEY (crime_report_dr_no) REFERENCES la_crimes.crime_report (dr_no),
  FOREIGN KEY (weapon_weapon_used_cd) REFERENCES la_crimes.weapon (weapon_used_cd)
);

CREATE TABLE IF NOT EXISTS la_crimes.victim (
  dr_no INTEGER NOT NULL,
  vict_age INTEGER NOT NULL,
  vict_sex VARCHAR(5) DEFAULT NULL,
  vict_descent VARCHAR(5) DEFAULT NULL,
  FOREIGN KEY (dr_no) REFERENCES la_crimes.crime_report (dr_no)
);