
CREATE TABLE Area (
  area_id INTEGER NOT NULL,
  area_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (area_id)
);

CREATE TABLE Crime_Location (
  location_id SERIAL PRIMARY KEY,
  location VARCHAR(100) NOT NULL,
  lat NUMERIC(10,7) NOT NULL,
  lon NUMERIC(10,7) NOT NULL,
  cross_street VARCHAR(100) DEFAULT NULL
);

CREATE TABLE  Status (
  status_code VARCHAR(10) PRIMARY KEY,
  status_desc VARCHAR(100) NOT NULL
);

CREATE TABLE Premises (
  premis_cd INTEGER PRIMARY KEY,
  premis_desc VARCHAR(100) NOT NULL
);

CREATE TABLE Reporting_Districts (
  rpt_dist_no INTEGER NOT NULL,
  area_id INTEGER NOT NULL,
  PRIMARY KEY (rpt_dist_no),
  FOREIGN KEY (area_id) REFERENCES Area(area_id)
);
-- -------------------------------------------------------------
CREATE TABLE Crime_code (
  crm_cd INTEGER,
  crm_cd_2 INTEGER,
  crm_cd_3 INTEGER,
  crm_cd_4 INTEGER,
  crm_cd_desc VARCHAR(100) NOT NULL,
  PRIMARY KEY (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4)
);
-- --------------------------------------------------------------
CREATE TABLE Crime_report (
  dr_no INTEGER PRIMARY KEY,
  date_rptd DATE NOT NULL,
  date_occ DATE NOT NULL,
  time_occ TIME NOT NULL,
  status_code VARCHAR(10) NOT NULL REFERENCES Status(status_code),
  premis_cd INTEGER NOT NULL REFERENCES Premises(premis_cd),
  rpt_dist_no INTEGER NOT NULL REFERENCES Reporting_District(rpt_dist_no), 
  area_id INTEGER NOT NULL REFERENCES Area(area_id),
  location_id INTEGER REFERENCES Crime_Location(location_id),
  mocodes VARCHAR(50),
  weapon_cd INTEGER REFERENCES Weapon(weapon_cd),
  crime_code_crm_cd INTEGER NOT NULL,
  crime_code_crm_cd_2 INTEGER,
  crime_code_crm_cd_3 INTEGER,
  crime_code_crm_cd_4 INTEGER,
  FOREIGN KEY (crime_code_crm_cd, crime_code_crm_cd_2, crime_code_crm_cd_3, crime_code_crm_cd_4) REFERENCES Crime_code (crm_cd, crm_cd_2, crm_cd_3, crm_cd_4)
);

CREATE TABLE Weapon (
  weapon_cd INTEGER PRIMARY KEY,
  weapon_desc VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Victim (
    vict_id SERIAL,
    dr_no INTEGER NOT NULL,
    vict_age INTEGER NOT NULL,
    vict_sex CHAR(1) DEFAULT NULL,
    vict_descent CHAR(2) DEFAULT NULL,
    PRIMARY KEY (vict_id, dr_no), -- Composite primary key
    FOREIGN KEY (dr_no) REFERENCES Crime_report(dr_no)
);
