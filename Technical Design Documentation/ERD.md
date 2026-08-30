# ERD

```mermaid
erDiagram
    CUSTOMERS ||--o{ RESERVATIONS : makes
    ROOM_TYPES ||--o{ ROOMS : defines
    RESERVATIONS ||--o{ RESERVATION_ROOMS : contains
    ROOMS ||--o{ RESERVATION_ROOMS : assigned_to

    CUSTOMERS {
        int customer_id PK
        varchar first_name
        varchar last_name
        varchar email "UNIQUE"
        varchar phone
        varchar password_hash
        datetime created_at
        datetime updated_at
    }

    RESERVATIONS {
        int reservation_id PK
        int customer_id FK
        int num_guests
        date check_in_date
        date check_out_date
        decimal total_price
        varchar reservation_status
        datetime created_at
        datetime updated_at
    }

    RESERVATION_ROOMS {
        int reservation_room_id PK
        int reservation_id FK
        int room_id FK
        decimal nightly_rate
    }

    ROOMS {
        int room_id PK
        int room_type_id FK
        varchar room_number "UNIQUE"
    }

    ROOM_TYPES {
        int room_type_id PK
        varchar room_type_name
        decimal price_per_night
        int max_occupancy
    }

    CONTACT_MESSAGES {
            int message_id PK
            varchar name
            varchar email
            varchar subject
            text message
            datetime created_at
        }
```

## Customers Table

| Column               | Type          | Constraints / Notes                          |
|----------------------|---------------|----------------------------------------------|
| customer_id          | INT           | PK, auto-increment                           |
| first_name           | VARCHAR(100)  | Required                                     |
| last_name            | VARCHAR(100)  | Required                                     |
| email                | VARCHAR(255)  | UNIQUE, required                             |
| phone                | VARCHAR(20)   | Optional                                     |
| password_hash        | VARCHAR(255)  | Required, hashed password                    |
| created_at           | DATETIME      | Default: current timestamp                   |
| updated_at           | DATETIME      | Default: current timestamp on update         |

## Reservations Table

| Column                   | Type          | Constraints / Notes                          |
|--------------------------|---------------|----------------------------------------------|
| reservation_id           | INT           | PK, auto-increment                           |
| customer_id              | INT           | FK → Customers.customer_id, required         |
| num_guests               | INT           | Required                                     |
| check_in_date            | DATE          | Required                                     |
| check_out_date           | DATE          | Required                                     |
| total_price              | DECIMAL(10,2) | Required                                     |
| reservation_status       | VARCHAR(20)   | Required                                     |
| created_at               | DATETIME      | Default: current timestamp                   |
| updated_at               | DATETIME      | Default: current timestamp on update         |

## ReservationRooms Table

| Column              | Type          | Constraints / Notes                          |
|---------------------|---------------|----------------------------------------------|
| reservation_room_id | INT           | PK, auto-increment                           |
| reservation_id      | INT           | FK → Reservations.reservation_id, required   |
| room_id             | INT           | FK → Rooms.room_id, required                 |
| nightly_rate        | DECIMAL(10,2) | Required                                     |

## Rooms Table

| Column         | Type         | Constraints / Notes                          |
|----------------|--------------|----------------------------------------------|
| room_id        | INT          | PK, auto-increment                           |
| room_type_id   | INT          | FK → Room_Types.room_type_id, required       |
| room_number    | VARCHAR(20)  | UNIQUE, required                             |

## RoomTypes Table

| Column           | Type          | Constraints / Notes                          |
|------------------|---------------|----------------------------------------------|
| room_type_id     | INT           | PK, auto-increment                           |
| room_type_name   | VARCHAR(50)   | Required                                     |
| price_per_night  | DECIMAL(10,2) | Required                                     |
| max_occupancy    | INT           | Required                                     |


## ContactMessages Table

| Column                   | Type          | Constraints / Notes                          |
|--------------------------|---------------|----------------------------------------------|
| message_id               | INT           | PK, auto-increment                           |
| name                     | VARCHAR(100)  | Required                                     |
| email                    | VARCHAR(100)  | Required                                     |
| subject                  | VARCHAR(100)  | Required                                     |
| message                  | Text          | Required                                     |
| created_at               | DATETIME      | Default: current timestamp                   |
