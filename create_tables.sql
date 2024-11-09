-- Create the area table
CREATE TABLE IF NOT EXISTS area (
  area_id INT PRIMARY KEY,
  area_name VARCHAR(50) NOT NULL
);

-- Create the status table
CREATE TABLE IF NOT EXISTS status (
  status VARCHAR(10) PRIMARY KEY,
  status_desc VARCHAR(100) NOT NULL
);

-- Create the premises table
CREATE TABLE IF NOT EXISTS premises (
  premis_cd INT PRIMARY KEY,
  premis_desc VARCHAR(100) NOT NULL
);

-- Create the reporting_district table
CREATE TABLE IF NOT EXISTS reporting_district (
  rpt_dist_no INT PRIMARY KEY,
  area_area_id INT NOT NULL,
  FOREIGN KEY (area_area_id) REFERENCES area (area_id)
);

-- Create the crime_location table
CREATE TABLE IF NOT EXISTS crime_location (
  location VARCHAR(100) PRIMARY KEY,
  lat DECIMAL(10,7) NOT NULL,
  lon DECIMAL(10,7) NOT NULL,
  cross_street VARCHAR(100)
);

-- Create the new crime_chronicle table
CREATE TABLE IF NOT EXISTS crime_chronicle (
    date_occ DATE NOT NULL,
    time_occ TIME NOT NULL,
    PRIMARY KEY (date_occ, time_occ)
);

-- Create the crime_report table
CREATE TABLE IF NOT EXISTS crime_report (
  dr_no INT PRIMARY KEY,
  date_rptd DATE NOT NULL,
  crime_chronicle_date_occ DATE NOT NULL,
  crime_chronicle_time_occ TIME NOT NULL,
  status_status VARCHAR(10) NOT NULL,
  premises_premis_cd INT NOT NULL,
  reporting_district_rpt_dist_no INT NOT NULL,
  area_area_id INT NOT NULL,
  crime_location_location VARCHAR(100) NOT NULL,
  FOREIGN KEY (status_status) REFERENCES status (status),
  FOREIGN KEY (premises_premis_cd) REFERENCES premises (premis_cd),
  FOREIGN KEY (reporting_district_rpt_dist_no) REFERENCES reporting_district (rpt_dist_no),
  FOREIGN KEY (area_area_id) REFERENCES area (area_id),
  FOREIGN KEY (crime_location_location) REFERENCES crime_location (location),
  FOREIGN KEY (crime_chronicle_date_occ , crime_chronicle_time_occ) REFERENCES crime_chronicle (date_occ, time_occ)
);

-- Create the crime_type table
CREATE TABLE IF NOT EXISTS crime_type (
  crm_cd INT PRIMARY KEY,
  crm_cd_desc VARCHAR(100) NOT NULL,
  mocodes VARCHAR(50),
  crm_cd_2 INT,
  crm_cd_3 INT,
  crm_cd_4 INT
);

-- Create the crime_incident_crime_code table
CREATE TABLE IF NOT EXISTS crime_incident_crime_code (
  dr_no INT NOT NULL,
  crm_cd INT NOT NULL,
  PRIMARY KEY (dr_no, crm_cd),
  FOREIGN KEY (dr_no) REFERENCES crime_report (dr_no),
  FOREIGN KEY (crm_cd) REFERENCES crime_type (crm_cd)
);

-- Create the weapon table
CREATE TABLE IF NOT EXISTS weapon (
  weapon_used_cd INT PRIMARY KEY,
  weapon_desc VARCHAR(100) NOT NULL
);


-- Create the crime_report_has_weapon table
CREATE TABLE IF NOT EXISTS crime_report_has_weapon (
  crime_report_dr_no INT NOT NULL,
  weapon_weapon_used_cd INT NOT NULL,
  PRIMARY KEY (crime_report_dr_no, weapon_weapon_used_cd),
  FOREIGN KEY (crime_report_dr_no) REFERENCES crime_report (dr_no),
  FOREIGN KEY (weapon_weapon_used_cd) REFERENCES weapon (weapon_used_cd)
);

-- Create the victim table
CREATE TABLE IF NOT EXISTS victim (
  dr_no INT NOT NULL,
  vict_age INT NOT NULL,
  vict_sex VARCHAR(5),
  vict_descent VARCHAR(5),
  FOREIGN KEY (dr_no) REFERENCES crime_report (dr_no)
);