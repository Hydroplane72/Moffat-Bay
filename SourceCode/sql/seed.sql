-- seed.sql
-- Sample data for Moffat Bay's hotel reservation system.

INSERT INTO Customers (first_name, last_name, email, phone, password_hash)
VALUES
('Demo', 'User', 'demo@moffatbay.com', '555-0101', SHA2('DemoPass1', 256)),
('Alice', 'Smith', 'alice@example.com', '555-0192', SHA2('Password123', 256)),
('Bob', 'Jones', 'bob@example.com', '555-0144', SHA2('Password123', 256)),
('Maria', 'Garcia', 'maria@example.com', '555-0117', SHA2('Password123', 256)),
('Lucia', 'Collins', 'lucia@example.com', '555-0139', SHA2('Password123', 256));

INSERT INTO RoomTypes (room_type_name, price_per_night, max_occupancy)
VALUES
('Double Full Beds', 120.00, 2),
('Queen', 135.00, 2),
('Double Queen Beds', 150.00, 4),
('King', 160.00, 2);

INSERT INTO Rooms (room_type_id, room_number, room_status)
VALUES
(1, '101', 'available'),
(1, '102', 'available'),
(1, '103', 'available'),
(1, '104', 'available'),
(1, '105', 'available'),
(2, '201', 'available'),
(2, '202', 'occupied'),
(2, '203', 'available'),
(2, '204', 'available'),
(2, '205', 'available'),
(3, '301', 'available'),
(3, '302', 'available'),
(3, '303', 'available'),
(3, '304', 'available'),
(3, '305', 'available'),
(4, '401', 'available'),
(4, '402', 'occupied'),
(4, '403', 'available'),
(4, '404', 'available'),
(4, '405', 'available');

INSERT INTO Reservations (customer_id, num_guests, check_in_date, check_out_date, total_price, reservation_status)
VALUES
(1, 2, '2026-09-10', '2026-09-13', 360.00, 'confirmed'),
(2, 2, '2026-09-15', '2026-09-18', 405.00, 'confirmed'),
(3, 4, '2026-09-20', '2026-09-23', 600.00, 'pending'),
(5, 2, '2026-09-25', '2026-09-28', 270.00, 'confirmed');

INSERT INTO ReservationRooms (reservation_id, room_id, nightly_rate)
VALUES
(1, 1, 120.00),
(2, 6, 135.00),
(3, 11, 150.00),
(4, 16, 160.00);