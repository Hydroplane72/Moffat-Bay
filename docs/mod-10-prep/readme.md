# How to Run Our Moffat Bay Lodge Website in Your Browser

This project uses HTML/CSS/JavaScript for the website, a Python API
server, and a MySQL database.

## Requirements

Before running the website, make sure you have:

-   Python installed
-   MySQL or MariaDB servers
-   The `moffat_bay` database created
-   A terminal such as Command Prompt, PowerShell, Terminal, or the VS
    Code terminal

## 1. Open the Project Folder

Extract the project ZIP file and open the main `RedTeam_CSD460`
folder in your IDE.

The folder you open should contain the `src` folder.

## 2. Install the Python Requirements

Open a terminal in the project root and run:

``` bash
python -m pip install -r src/api/requirements.txt
```

The project requires:

-   `mysql-connector-python`
-   `python-dotenv`

If `python` is not recognized on Windows, try:

``` bash
py -m pip install -r src/api/requirements.txt
```

## 3. Set Up the MySQL Database

Make sure your MySQL or MariaDB server is running.

Run the following SQL files in this order:

1.  `src/sql/schema.sql`
2.  `src/sql/seed.sql`

`schema.sql` creates the `moffat_bay` database and its tables.
`seed.sql` adds sample data used for development and testing.

> **Warning:** `schema.sql` begins by dropping the existing `moffat_bay`
> database. If your team's database is named the same, please save it
> before running our project.

## 4. Configure the Database Connection

Open:

``` text
src/api/.env
```

Change the values match your local MySQL information:

``` env
MOFFAT_DB_HOST=localhost
MOFFAT_DB_PORT=3306
MOFFAT_DB_USER=YOUR_MYSQL_USERNAME
MOFFAT_DB_PASSWORD=YOUR_MYSQL_PASSWORD
MOFFAT_DB_NAME=moffat_bay
```

Replace `YOUR_MYSQL_USERNAME` and `YOUR_MYSQL_PASSWORD` with your own
MySQL login information.


## 5. Start the Website Server

From the **project root**, run:

``` bash
python src/api/startup_api.py
```

On Windows, you can also use:

``` bash
py src/api/startup_api.py
```

When the server starts successfully, the terminal should display the
website address and API addresses.

Keep this terminal window open while using the website.

## 6. Open the Website in a Browser

Open this address in Chrome, Edge, Safari, or Firefox:

``` text
http://127.0.0.1:8000/
```

The server automatically loads `src/index.html`.

Do **not** double-click `index.html` when testing the complete
application. Running the site through `startup_api.py` ensures the
website and APIs use the same local server.

## Sample Login

After loading `seed.sql`, one test account is:

``` text
Email: demo@moffatbay.com
Password: DemoPass1
```

If you want to create your own account you may.

## Stopping the Server

Return to the terminal running the website and press:

``` text
Ctrl + C
```

## Troubleshooting

### `python` is not recognized

Install Python and make sure it is added to your system PATH. On
Windows, try using `py` instead of `python`.

### Missing Python module

Run:

``` bash
python -m pip install -r src/api/requirements.txt
```

### Database connection error

Check that:

-   MySQL is running.
-   The username and password in `src/api/.env` are correct.
-   MySQL is using the port listed in `.env`, normally `3306`.
-   The `moffat_bay` database exists.
-   `schema.sql` and `seed.sql` were successfully executed.

### If your Port 8000 is already in use

Close the program already using port 8000, or change the server port by
setting `MOFFAT_SERVER_PORT` in `src/api/.env`. If you change the port,
also update `API_BASE_URL` in `src/assets/js/api-config.js` so the
browser sends API requests to the same port.

## Quick Start

Once the database has already been configured, starting the project
normally only requires:

``` bash
python src/api/startup_api.py
```

Then visit:

``` text
http://127.0.0.1:8000/
```
