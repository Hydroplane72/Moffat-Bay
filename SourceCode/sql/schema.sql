-- schema.sql - use to create the database schema for the hotel reservation system

DROP DATABASE IF EXISTS moffat_bay;
CREATE DATABASE moffat_bay;
USE moffat_bay;

CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(100) NOT NULL UNIQUE,
    customer_phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE RoomType (
    room_type_id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    max_occupancy INT NOT NULL
);

CREATE TABLE Rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    room_type_id INT NOT NULL,
    room_status VARCHAR(20) DEFAULT 'available',
    FOREIGN KEY (room_type_id) REFERENCES RoomType(room_type_id) ON DELETE RESTRICT
);

CREATE TABLE Reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    num_guests INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_reservation_price DECIMAL(10, 2) NOT NULL,
    reservation_status VARCHAR(20) DEFAULT 'confirmed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE ReservationRooms (
    reservation_room_id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    room_id INT NOT NULL,
    nightly_rate DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (reservation_id) REFERENCES Reservations(reservation_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE RESTRICT
);