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
    allow_reservations BIT NOT NULL DEFAULT 1,
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

CREATE TABLE ContactMessages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- view to see room availability
CREATE VIEW room_availability_base AS
SELECT
    r.room_id,
    r.room_number,
    rt.room_type_name,
    r.allow_reservations,
    res.reservation_id,
    res.check_in_date,
    res.check_out_date,
    res.reservation_status
FROM Rooms r
LEFT JOIN RoomTypes rt 
    ON r.room_type_id = rt.room_type_id
LEFT JOIN ReservationRooms rr 
    ON r.room_id = rr.room_id
LEFT JOIN Reservations res 
    ON rr.reservation_id = res.reservation_id;
    
-- Stored proc to get room availability by a date range
-- This should return ALL rooms in the date ranges and whether they are available or not for each day in the date range.
DELIMITER $$

CREATE PROCEDURE get_room_availability(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    WITH RECURSIVE date_range AS (
        SELECT p_start_date AS d
        UNION ALL
        SELECT DATE_ADD(d, INTERVAL 1 DAY)
        FROM date_range
        WHERE d < p_end_date
    )
    SELECT
        dr.d AS calendar_date,
        r.room_id,
        r.room_number,
        r.room_type_name,
        r.allow_reservations,
        CASE
            WHEN r.allow_reservations = 0 THEN 'Unavailable'
            WHEN EXISTS (
                SELECT 1
                FROM room_availability_base b
                WHERE b.room_id = r.room_id
                  AND b.reservation_status = 'confirmed'
                  AND dr.d BETWEEN b.check_in_date AND b.check_out_date
            )
            THEN 'Unavailable'
            ELSE 'Available'
        END AS availability_status
    FROM date_range dr
    CROSS JOIN (
        SELECT DISTINCT room_id, room_number, room_type_name, allow_reservations
        FROM room_availability_base
    ) r
    ORDER BY dr.d, r.room_number;
END $$

DELIMITER ;




