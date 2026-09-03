# Tiffany's Landing Page Setup

## Files Added or Updated

- `src/index.html` - production landing page markup and safe fallback room cards.
- `src/assets/js/landing.js` - mobile navigation plus dynamic room data loading.
- `src/api/landing_api.py` - Python web server and MySQL-backed room type endpoint.
- `src/api/tests/test_landing_api.py` - exactly two functional development tests.
- `docs/LandingPageFunctionalTests.md` - test cases and screenshot instructions.

## Install the Python Dependency

```text
python -m pip install mysql-connector-python pytest
```

## Run the Landing Page

From the Moffat-Bay project folder:

```text
python src/api/landing_api.py
```

Open `http://127.0.0.1:8000/` in the browser.

## Run the Two Functional Tests

```text
python -m pytest src/api/tests/test_landing_api.py -v
```

## What the Backend Does

The landing page displays room names and nightly prices. Those values belong in the database rather than being trusted only as hard-coded HTML. The endpoint `GET /api/landing/room-types` reads `room_type_id`, `room_type_name`, `price_per_night`, and `max_occupancy` from the shared `RoomTypes` table. The browser loads that JSON and rebuilds the four room cards.

The original HTML room cards remain as a safe fallback. If MySQL is unavailable, the page still displays basic room information and gives the visitor a clear message that live pricing is temporarily unavailable.
