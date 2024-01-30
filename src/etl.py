import sqlite3
import pandas as pd
import numpy as np
import os

# Paths to the raw data folders
raw_data_paths = ["../data/raw/2021", "../data/raw/2022"]

# Path to the output folder
processed_data_path = "../data/processed"

# Column names for the CSV files
column_names = ["kod_stacji", "nazwa_stacji", "rok", "miesiac", "dzien", "max_temp_dobowa",
                "status_pomiaru_tmax", "min_temp_dobowa", "status_pomiaru_tmin", "srednia_temp_dobowa",
                "status_pomiaru_std", "min_temp_przy_gruncie", "status_pomiaru_tmng", "suma_dobowa_opadow",
                "status_pomiaru_smdb", "rodzaj_opadu", "wysokosc_pokrywy_snieznej", "status_pomiaru_pksn"]

# Loop through each raw data folder
for path in raw_data_paths:

    # DataFrame to store data from each folder of raw data
    df_processed = pd.DataFrame()

    # Loop through each file in the folder
    for file in os.listdir(path):

        # Reading the CSV file into a Pandas DataFrame
        df = pd.read_csv(os.path.join(path, file), header=None, encoding='ISO-8859-2')

        # Adding column names
        df.columns = column_names

        cols_to_remove = ["kod_stacji", "nazwa_stacji", "rok", "miesiac", "rodzaj_opadu", "dzien", "status_pomiaru_tmng", "status_pomiaru_std", "status_pomiaru_pksn",
                         "status_pomiaru_tmax", "status_pomiaru_smdb", "status_pomiaru_tmin"]

        for col in cols_to_remove:
            try:
                df.drop(columns=[col], inplace=True)
            except KeyError:
                pass

        # Filling missing data with mean for numeric data
        numeric_cols = df.select_dtypes(include=[np.number])
        df[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())

        # Filling remaining missing data
        # This uses a deprecated method, should be changed to something else
        df.fillna(method='ffill', inplace=True)

        # Creating target variable based on current data
        df["czy_pada"] = df["suma_dobowa_opadow"].apply(lambda x: 1 if x > 0 else 0)

        # Moving all data except 'czy_pada' down by 1 row
        df.loc[:, df.columns != 'czy_pada'] = df.loc[:, df.columns != 'czy_pada'].shift(-1)

        # Removing last row with NaN
        df.dropna(inplace=True)

        # Removing empty columns
        df = df.dropna(axis=1, how='all')

        # Removing empty rows
        df = df.dropna(axis=0, how='all')

        # Appending the processed data to the output DataFrame
        # Apparently append got deprecated, so I used concat instead
        df_processed = pd.concat([df_processed, df], ignore_index=True)

    # Writing the processed data to a single CSV file
    output_file = os.path.join(processed_data_path, f"{os.path.basename(path)}_processed.csv")
    df_processed.to_csv(output_file, index=False, encoding='ISO-8859-2')

# Loop through each file in the folder
for filename in os.listdir(processed_data_path):
    if filename.endswith('.csv'):
        # Path to the CSV file
        file_path = os.path.join(processed_data_path, filename)

        # Loading the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path, encoding='ISO-8859-2')

        # Path to the database file
        db_file = "../data/processed/processed_data.db"

        # Connecting to the database
        conn = sqlite3.connect(db_file)

        # Saving the DataFrame to the database
        df.to_sql('processed_data', conn, if_exists='replace', index=False)

        # Close the database connection
        conn.close()

