import sqlite3

from src.Weather import WeatherCreate

# Define the path to the database file
db_file = "../data/processed/processed_data.db"


def create_connection():
    connection = sqlite3.connect("processed_data.db")
    return connection


def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    max_temp_dobowa REAL,
    min_temp_dobowa REAL,
    srednia_temp_dobowa REAL,
    min_temp_przy_gruncie REAL,
    suma_dobowa_opadow REAL,
    wysokosc_pokrywy_snieznej REAL
    )""")
    connection.commit()
    connection.close()


def add_weather(weather: WeatherCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO processed_data (max_temp_dobowa, min_temp_dobowa, srednia_temp_dobowa, "
                   "min_temp_przy_gruncie, suma_dobowa_opadow, wysokosc_pokrywy_snieznej) VALUES (?, ?, ?, ?, ?, ?)",
                   (weather.max_temp_dobowa, weather.min_temp_dobowa, weather.srednia_temp_dobowa,
                    weather.min_temp_przy_gruncie, weather.suma_dobowa_opadow, weather.wysokosc_pokrywy_snieznej))
    connection.commit()
    connection.close()
