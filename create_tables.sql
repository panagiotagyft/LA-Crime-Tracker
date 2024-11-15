CREATE TABLE IF NOT EXISTS Area (
  area_id INTEGER NOT NULL,
  area_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (area_id)
);

CREATE TABLE IF NOT EXISTS Crime_Location (
  location_id SERIAL PRIMARY KEY,
  location VARCHAR(100) NOT NULL,
  lat NUMERIC(10,7) NOT NULL,
  lon NUMERIC(10,7) NOT NULL,
  cross_street VARCHAR(100) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS Status (
  status_code VARCHAR(10) PRIMARY KEY,
  status_desc VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Premises (
  premis_cd INTEGER PRIMARY KEY,
  premis_desc VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Reporting_Districts (
  rpt_dist_no INTEGER NOT NULL,
  area_id INTEGER NOT NULL,
  PRIMARY KEY (rpt_dist_no),
  FOREIGN KEY (area_id) REFERENCES Area(area_id)
);
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS crime_code (
  crm_cd INTEGER NOT NULL,
  crm_cd_desc VARCHAR(100) NOT NULL,
  crm_cd_2 INTEGER NOT NULL DEFAULT -1,
  crm_cd_3 INTEGER NOT NULL DEFAULT -1,
  crm_cd_4 INTEGER NOT NULL DEFAULT -1,
  PRIMARY KEY (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4)
);
-- --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS crime_report (
  dr_no INTEGER PRIMARY KEY,
  date_rptd DATE NOT NULL,
  date_occ DATE NOT NULL,
  time_occ TIME NOT NULL,
  status_code VARCHAR(10) NOT NULL REFERENCES Status(status_code),
  premis_cd INTEGER NOT NULL REFERENCES Premises(premis_cd),
  rpt_dist_no INTEGER NOT NULL REFERENCES Reporting_District(rpt_dist_no), 
  area_id INTEGER NOT NULL REFERENCES Area(area_id),
  location_id INTEGER REFERENCES Crime_Location(location_id);
  mocodes VARCHAR(50),
  crime_type_crm_cd INTEGER NOT NULL,
  crime_type_crm_cd_2 INTEGER NOT NULL DEFAULT -1,
  crime_type_crm_cd_3 INTEGER NOT NULL DEFAULT -1,
  crime_type_crm_cd_4 INTEGER NOT NULL DEFAULT -1,
  FOREIGN KEY (crime_type_crm_cd, crime_type_crm_cd_2, crime_type_crm_cd_3, crime_type_crm_cd_4) REFERENCES crime_type (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4)
);

CREATE TABLE IF NOT EXISTS Weapon (
  weapon_used_cd INTEGER NOT NULL PRIMARY KEY,
  weapon_desc VARCHAR(100) NOT NULL,
);

CREATE TABLE IF NOT EXISTS Crime_Report_has_Weapon (
  dr_no INTEGER NOT NULL REFERENCES Crime_Report(dr_no),
  weapon_used_cd INTEGER NOT NULL REFERENCES Weapon(weapon_used_cd),
  PRIMARY KEY (crime_report_dr_no, weapon_weapon_used_cd)
);

CREATE TABLE IF NOT EXISTS Victim (
  dr_no INTEGER NOT NULL REFERENCES Crime_Report(dr_no),
  vict_age INTEGER NOT NULL,
  vict_sex VARCHAR(5) DEFAULT NULL,
  vict_descent VARCHAR(5) DEFAULT NULL
);