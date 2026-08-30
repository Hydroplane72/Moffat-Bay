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

INSERT INTO Rooms (room_id, room_type_id, room_number)
VALUES
(1, 1, '101'),
(2, 1, '102'),
(3, 1, '103'),
(4, 1, '104'),
(5, 1, '105'),
(6, 2, '201'),
(7, 2, '202'),
(8, 2, '203'),
(9, 2, '204'),
(10, 2, '205'),
(11, 3, '301'),
(12, 3, '302'),
(13, 3, '303'),
(14, 3, '304'),
(15, 3, '305'),
(16, 4, '401'),
(17, 4, '402'),
(18, 4, '403'),
(19, 4, '404'),
(20, 4, '405');

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