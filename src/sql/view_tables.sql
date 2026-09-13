-- Project: Moffat Bay Lodge
-- Course: CSD 460
-- Team Name: Red Team
-- Team Members:
--   Brayan Covarrubias
--   Matthew Rozendaal
--   Rashai Robertson
--   Tiffany Davidson
-- File: view_tables.sql
-- Purpose: Provides read-only queries used to review the contents of the Moffat Bay database tables during testing.

USE moffat_bay;

SELECT * FROM Customers;

SELECT * FROM RoomTypes;

SELECT * FROM Rooms;

SELECT * FROM Reservations;

SELECT * FROM ReservationRooms;

SELECT * FROM ContactMessages;
