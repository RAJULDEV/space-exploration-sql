CREATE DATABASE IF NOT EXISTS space_exploration;
USE space_exploration;

CREATE TABLE agencies (
    agency_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50)
);

CREATE TABLE missions (
    mission_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    launch_date DATETIME,
    agency_id INT,
    success BOOLEAN,
    destination VARCHAR(50),
    mission_type VARCHAR(50),
    cost DECIMAL(10, 2),
    FOREIGN KEY (agency_id) REFERENCES agencies(agency_id)
);