import pandas as pd
import os

# Define the paths to the raw data folders
raw_data_paths = ["../data/raw/2021", "../data/raw/2022"]

# Define the path to the output folder
output_path = "../data/processed"

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

        df.drop(columns=["status_pomiaru_tmng", "status_pomiaru_std", "status_pomiaru_pksn",
                         "status_pomiaru_tmax", "status_pomiaru_smdb", "status_pomiaru_tmin"], inplace=True)

        # Removing empty columns
        #df = df.dropna(axis=1, how='all')

        # Removing empty rows
        #df = df.dropna(axis=0, how='all')

        # Appending the processed data to the output DataFrame
        # Apparently append got deprecated, so I used concat instead
        df_processed = pd.concat([df_processed, df], ignore_index=True)

    # Writing the processed data to a single CSV file
    output_file = os.path.join(output_path, f"{os.path.basename(path)}_processed.csv")
    df_processed.to_csv(output_file, index=False, encoding='ISO-8859-2')
