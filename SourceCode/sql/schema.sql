-- schema.sql 
-- Use to create the database schema for Moffat Bay's hotel reservation system.

DROP DATABASE IF EXISTS moffat_bay;
CREATE DATABASE moffat_bay;
USE moffat_bay;

CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE RoomTypes (
    room_type_id INT AUTO_INCREMENT PRIMARY KEY,
    room_type_name VARCHAR(50) NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL CHECK (price_per_night > 0),
    max_occupancy INT NOT NULL CHECK (max_occupancy > 0)
);

CREATE TABLE Rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_type_id INT NOT NULL,
    room_number VARCHAR(20) NOT NULL UNIQUE,
    room_status VARCHAR(20) NOT NULL DEFAULT 'available',
    FOREIGN KEY (room_type_id) REFERENCES RoomTypes(room_type_id) ON DELETE RESTRICT
);

CREATE TABLE Reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    num_guests INT NOT NULL CHECK (num_guests > 0),
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL CHECK (total_price >= 0),
    reservation_status VARCHAR(20) NOT NULL DEFAULT 'confirmed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (check_out_date > check_in_date),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE ReservationRooms (
    reservation_room_id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    room_id INT NOT NULL,
    nightly_rate DECIMAL(10, 2) NOT NULL CHECK (nightly_rate >= 0),
    FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE RESTRICT
);