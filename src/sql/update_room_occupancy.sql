USE moffat_bay;

UPDATE RoomTypes SET max_occupancy = 4 WHERE room_type_name = 'Double Full Beds';
UPDATE RoomTypes SET max_occupancy = 2 WHERE room_type_name = 'Queen';
UPDATE RoomTypes SET max_occupancy = 6 WHERE room_type_name = 'Double Queen Beds';
UPDATE RoomTypes SET max_occupancy = 2 WHERE room_type_name = 'King';

SELECT room_type_name, max_occupancy
FROM RoomTypes
ORDER BY room_type_id;
