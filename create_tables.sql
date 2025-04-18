CREATE TABLE custom_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL
);

CREATE TABLE custom_token (
    key VARCHAR(40) PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES custom_user(id) ON DELETE CASCADE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


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

CREATE TABLE IF NOT EXISTS  Status (
  status_code VARCHAR(10) PRIMARY KEY,
  status_desc VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Premises (
  premis_cd INTEGER PRIMARY KEY,
  premis_desc VARCHAR(100) NOT NULL
);

-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Crime_code (
  crm_cd_id SERIAL PRIMARY KEY,
  crm_cd INTEGER,
  crm_cd_desc VARCHAR(100)
);
-- ------------------------------------------
CREATE TABLE IF NOT EXISTS Weapon(
  weapon_cd INTEGER PRIMARY KEY,
  weapon_desc VARCHAR(100)
);
--------------------------------------------
CREATE TABLE IF NOT EXISTS Timestamp (
  timestamp_id SERIAL PRIMARY KEY,
  date_occ DATE NOT NULL,
  time_occ TIME NOT NULL
);
-- --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Crime_report (
  dr_no BIGINT PRIMARY KEY,
  date_rptd DATE NOT NULL,
  timestamp_id INTEGER NOT NULL REFERENCES Timestamp(timestamp_id),
  status_code VARCHAR(10) NOT NULL REFERENCES Status(status_code),
  premis_cd INTEGER NOT NULL REFERENCES Premises(premis_cd),
  rpt_dist_no INTEGER NOT NULL, 
  area_id INTEGER NOT NULL REFERENCES Area(area_id),
  location_id INTEGER REFERENCES Crime_Location(location_id),
  mocodes VARCHAR(50),
  weapon_cd INTEGER REFERENCES Weapon(weapon_cd),
  crm_cd INTEGER NOT NULL REFERENCES Crime_code(crm_cd_id),
  crm_cd_2 INTEGER REFERENCES Crime_code(crm_cd_id),
  crm_cd_3 BIGINT REFERENCES Crime_code(crm_cd_id),
  crm_cd_4 BIGINT REFERENCES Crime_code(crm_cd_id)
);
--------------------------------------
CREATE TABLE IF NOT EXISTS Victim (
    vict_id SERIAL,
    dr_no INTEGER NOT NULL,
    vict_age INTEGER NOT NULL,
    vict_sex VARCHAR(10) DEFAULT NULL,
    vict_descent VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY (vict_id, dr_no), -- Composite primary key
    FOREIGN KEY (dr_no) REFERENCES Crime_report(dr_no)
);

-- Index for crime date and time
CREATE INDEX IF NOT EXISTS idx_date_occ ON Timestamp(date_occ);
CREATE INDEX IF NOT EXISTS idx_time_occ ON Timestamp(time_occ);
CREATE INDEX IF NOT EXISTS idx_crime_report_timestamp_id ON Crime_report(timestamp_id);

CREATE INDEX IF NOT EXISTS idx_crime_code_crm_cd ON Crime_code(crm_cd);

-- Index for primary crime code
CREATE INDEX IF NOT EXISTS idx_crm_cd ON Crime_report(crm_cd);

-- Indexes for secondary crime codes
CREATE INDEX IF NOT EXISTS idx_crm_cd_2 ON Crime_report(crm_cd_2);
CREATE INDEX IF NOT EXISTS idx_crm_cd_3 ON Crime_report(crm_cd_3);
CREATE INDEX IF NOT EXISTS idx_crm_cd_4 ON Crime_report(crm_cd_4);

-- Index for area (Area ID)
CREATE INDEX IF NOT EXISTS idx_area_id ON Crime_report(area_id);
CREATE INDEX IF NOT EXISTS idx_area_name ON Area(area_name);

-- Indexes for geographic data (Latitude and Longitude)
CREATE INDEX IF NOT EXISTS idx_lat_lon ON Crime_Location(lat, lon);

-- Index for victim's age
CREATE INDEX IF NOT EXISTS idx_vict_age ON Victim(vict_age);

-- Index for crime status code
CREATE INDEX IF NOT EXISTS idx_status_code ON Crime_report(status_code);

-- Index for weapon type
CREATE INDEX IF NOT EXISTS idx_weapon_cd ON Crime_report(weapon_cd);

CREATE INDEX IF NOT EXISTS idx_crime_report_date_rptd ON Crime_Report(date_rptd);
CREATE INDEX IF NOT EXISTS idx_crime_report_rpt_dist_no ON Crime_report(rpt_dist_no);
