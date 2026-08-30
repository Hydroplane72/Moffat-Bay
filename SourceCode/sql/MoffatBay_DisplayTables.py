"""
Moffat Bay SQL Table Display Script

Purpose:
    Connect to the local Moffat Bay MySQL database and display each SQL table
    one at a time in a clean terminal format.

    This makes it easy to take screenshots of the database tables for
    project documentation and place them into a Word document.

Setup:
    1. Make sure MySQL Server 8.0 is running.
    2. Make sure schema.sql has been run to create the moffat_bay database.
    3. Make sure seed.sql has been run to add the sample data.
    4. Install the MySQL connector if needed:

       python -m pip install mysql-connector-python

    5. Run this program from the Moffat-Bay project folder:

       python SourceCode\\sql\\MoffatBay_DisplayTables.py

Security:
    The MySQL password is requested when the program starts.
    The password is NOT stored in this Python file.
"""

import os
import sys
from getpass import getpass
from datetime import date, datetime
from decimal import Decimal


# ------------------------------------------------------------
# DATABASE SETTINGS
# ------------------------------------------------------------

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_NAME = "moffat_bay"


# Maximum number of characters displayed for a single value.
# This keeps very long values, such as password hashes or messages,
# from making the terminal table too wide for screenshots.
MAX_VALUE_WIDTH = 28


# ------------------------------------------------------------
# SCREEN DISPLAY FUNCTIONS
# ------------------------------------------------------------

def clear_screen():
    """
    Clear the terminal screen.

    This allows each database table to appear by itself,
    making screenshots easier to capture.
    """
    os.system("cls" if os.name == "nt" else "clear")


def format_value(value):
    """
    Convert values returned from MySQL into readable text.

    NULL values, decimal values, dates, byte values, and long
    strings are formatted so they display cleanly in the terminal.
    """

    if value is None:
        text = "NULL"

    elif isinstance(value, (bytes, bytearray)):
        # MySQL BIT fields may be returned as bytes.
        text = str(int.from_bytes(value, byteorder="big"))

    elif isinstance(value, Decimal):
        text = f"{value:.2f}"

    elif isinstance(value, (date, datetime)):
        text = str(value)

    else:
        text = str(value)

        # Remove line breaks so each SQL record remains on one line.
        text = text.replace("\n", " ").replace("\r", " ")

    # Shorten extremely long values for screenshot readability.
    if len(text) > MAX_VALUE_WIDTH:
        return text[:MAX_VALUE_WIDTH - 3] + "..."

    return text


def print_table(table_name, columns, rows):
    """
    Display one SQL table in a bordered terminal format.
    """

    formatted_rows = []

    for row in rows:
        formatted_row = []

        for value in row:
            formatted_row.append(format_value(value))

        formatted_rows.append(formatted_row)

    # Determine the width needed for each column.
    widths = []

    for index, column in enumerate(columns):

        longest_value = max(
            [
                len(formatted_row[index])
                for formatted_row in formatted_rows
            ],
            default=0,
        )

        column_width = max(
            len(column),
            longest_value
        )

        column_width = min(
            MAX_VALUE_WIDTH,
            column_width
        )

        widths.append(column_width)

    def border():
        """Create the horizontal border for the table."""

        return "+-" + "-+-".join(
            "-" * width
            for width in widths
        ) + "-+"

    def row_line(values):
        """Create one formatted table row."""

        cells = []

        for index, value in enumerate(values):
            cells.append(
                value.ljust(widths[index])
            )

        return "| " + " | ".join(cells) + " |"

    print("=" * 78)
    print("MOFFAT BAY DATABASE")
    print("=" * 78)
    print(f"Database: {DB_NAME}")
    print(f"Table:    {table_name}")
    print(f"Rows:     {len(rows)}")
    print("=" * 78)
    print()

    if not columns:
        print("No columns were returned.")
        return

    print(border())
    print(row_line(columns))
    print(border())

    if rows:

        for formatted_row in formatted_rows:
            print(row_line(formatted_row))

    else:

        empty_row = ["(no rows)"]

        for _ in columns[1:]:
            empty_row.append("")

        print(row_line(empty_row))

    print(border())
    print()


# ------------------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------------------

def connect_to_database():
    """
    Connect to the local Moffat Bay MySQL database.

    The user is prompted for the MySQL password when the
    program runs. The password is not stored in this file.
    """

    try:
        import mysql.connector
        from mysql.connector import Error

    except ImportError:

        print()
        print("ERROR: mysql-connector-python is not installed.")
        print()
        print("Install it using:")
        print()
        print("python -m pip install mysql-connector-python")
        print()

        input("Press Enter to exit...")
        sys.exit(1)

    print()
    print("=" * 60)
    print("MOFFAT BAY DATABASE CONNECTION")
    print("=" * 60)
    print()
    print(f"MySQL User: {DB_USER}")
    print(f"Database:   {DB_NAME}")
    print()

    # The password will not appear on the screen while it is typed.
    password = getpass("Enter your MySQL password: ")

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=password,
            database=DB_NAME,
        )

        print()
        print("Successfully connected to the Moffat Bay database.")

        return connection

    except Error as error:

        print()
        print("=" * 60)
        print("DATABASE CONNECTION ERROR")
        print("=" * 60)
        print()
        print("Could not connect to the Moffat Bay database.")
        print()
        print(f"MySQL error: {error}")
        print()
        print("Check the following:")
        print()
        print("1. MySQL Server 8.0 is running.")
        print("2. Your MySQL password is correct.")
        print("3. The moffat_bay database has been created.")
        print("4. schema.sql has been run.")
        print("5. seed.sql has been run.")
        print()

        input("Press Enter to exit...")
        sys.exit(1)


# ------------------------------------------------------------
# DATABASE QUERY FUNCTIONS
# ------------------------------------------------------------

def get_base_tables(connection):
    """
    Retrieve all base-table names from the moffat_bay database.
    """

    cursor = connection.cursor()

    try:

        query = """
            SELECT TABLE_NAME
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = %s
              AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME;
        """

        cursor.execute(
            query,
            (DB_NAME,)
        )

        results = cursor.fetchall()

        tables = []

        for row in results:
            tables.append(row[0])

        return tables

    finally:
        cursor.close()


def get_table_data(connection, table_name):
    """
    Retrieve every column and row from a database table.
    """

    cursor = connection.cursor()

    try:

        # Table names come directly from information_schema.
        query = f"SELECT * FROM `{table_name}`;"

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        return columns, rows

    finally:
        cursor.close()


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

def main():
    """
    Connect to MySQL and display every Moffat Bay table
    one at a time.
    """

    connection = connect_to_database()

    try:

        tables = get_base_tables(connection)

        if not tables:

            print()
            print(
                f"No SQL tables were found in database '{DB_NAME}'."
            )
            print()
            print("Make sure schema.sql has been run.")

            input("Press Enter to exit...")
            return

        total_tables = len(tables)

        for index, table_name in enumerate(
            tables,
            start=1
        ):

            clear_screen()

            columns, rows = get_table_data(
                connection,
                table_name
            )

            print()
            print(
                f"TABLE {index} OF {total_tables}"
            )
            print()

            print_table(
                table_name,
                columns,
                rows
            )

            print(
                "Take a screenshot of this table for your Word document."
            )
            print()

            if index < total_tables:

                input(
                    "Press Enter to display the next table..."
                )

            else:

                input(
                    "Press Enter to finish..."
                )

        clear_screen()

        print()
        print("=" * 60)
        print("MOFFAT BAY DATABASE DISPLAY COMPLETE")
        print("=" * 60)
        print()
        print(
            f"Successfully displayed {total_tables} SQL tables."
        )
        print()
        print(
            "You can now place the screenshots into your Word document."
        )
        print()

    finally:

        if connection.is_connected():
            connection.close()


# ------------------------------------------------------------
# PROGRAM START
# ------------------------------------------------------------

if __name__ == "__main__":
    main()