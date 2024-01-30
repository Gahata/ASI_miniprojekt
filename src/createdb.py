import sqlite3

# Define the path to the database file
db_file = "../data/processed/processed_data.db"

# Define the SQL statement to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS processed_data (
    max_temp_dobowa REAL,
    min_temp_dobowa REAL,
    srednia_temp_dobowa REAL,
    min_temp_przy_gruncie REAL,
    suma_dobowa_opadow REAL,
    wysokosc_pokrywy_snieznej REAL
);
"""

# Create a connection to the database
conn = sqlite3.connect(db_file)

# Create the table
conn.execute(create_table_sql)

# Commit the changes
conn.commit()

# Close the connection
conn.close()
