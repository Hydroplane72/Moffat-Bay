# ERD

## Customer Table

| Column        | Type          | Constraints / Notes                          |
|---------------|---------------|----------------------------------------------|
| customer_id   | INT           | PK, auto-increment                           |
| email         | VARCHAR(255)  | UNIQUE, required                             |
| first_name    | VARCHAR(100)  | Required                                     |
| last_name     | VARCHAR(100)  | Required                                     |
| telephone     | VARCHAR(20)   | Optional                                     |
| password_hash | VARCHAR(255)  | Required, hashed password                    |
| created_at    | DATETIME      | Default: current timestamp                   |
| updated_at    | DATETIME      | Default: current timestamp on update         |


## RoomType Table

| Column          | Type          | Constraints / Notes                          |
|-----------------|---------------|----------------------------------------------|
| room_type_id    | INT           | PK, auto-increment                           |
| name            | VARCHAR(100)  | Required                                     |
| price_per_night | DECIMAL(10,2) | Required                                     |
| max_num_rooms   | INT           | Required                                     |


## Reservation Table

| Column          | Type          | Constraints / Notes                          |
|-----------------|---------------|----------------------------------------------|
| reservation_id  | INT           | PK, auto-increment                           |
| customer_id     | INT           | FK → Customer.customer_id, required          |
| room_type_id    | INT           | FK → RoomType.room_type_id, required         |
| num_guests      | INT           | Required                                     |
| check_in_date   | DATE          | Required                                     |
| check_out_date  | DATE          | Required                                     |
| total_price     | DECIMAL(10,2) | Required                                     |
| created_at      | DATETIME      | Default: current timestamp                   |


## General Notes:
- There is a limitation on this ERD. The `RoomType` table has a `max_num_rooms` column, but there is no table to track individual rooms or their availability. This means that the system cannot track which specific rooms are booked or available, only the types of rooms and their maximum availability.
- If a user wants to book multiple rooms of the same type, the system will need to check if the total number of rooms booked for that type does not exceed `max_num_rooms`. 
- If a user wants to book multiple rooms of different types, the system will need to check the availability for each room type separately.
- If a user wants to book a room for multiple nights, the system will need to check the availability for each night of the stay. This means that the system will need to track the number of rooms booked for each room type on each date.
- If a user wants to book multiple rooms of the same type, then multiple reservations will need to be created. The Reservation table does not currently support multiple rooms of the same type in a single reservation. 
