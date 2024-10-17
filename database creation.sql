CREATE DATABASE airline_scheduling;

USE airline_scheduling;

CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(20) NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL
);

CREATE TABLE cargo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id VARCHAR(20) NOT NULL,
    description VARCHAR(255) NOT NULL,
    weight DECIMAL(10, 2) NOT NULL
);
