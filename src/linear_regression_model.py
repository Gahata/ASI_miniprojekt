import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from joblib import dump


def prepare_data(df):

    # Removing unnecessary columns
    try:
        df.drop(columns=["kod_stacji", "nazwa_stacji", "rok", "miesiac", "rodzaj_opadu", "dzien"], inplace=True)
    except:
        pass

    # Fill missing data with mean for numeric data
    numeric_cols = df.select_dtypes(include=[np.number])
    df[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())

    # Fill remaining missing data
    df.fillna(method='ffill', inplace=True)

    # Creating target variable based on current data
    df["czy_pada"] = df["suma_dobowa_opadow"].apply(lambda x: 1 if x > 0 else 0)

    # Moving all data except 'czy_pada' down by 1 row
    df.loc[:, df.columns != 'czy_pada'] = df.loc[:, df.columns != 'czy_pada'].shift(-1)

    # Removing last row with NaN
    df.dropna(inplace=True)

    return df


# Loading and checking data
def load_and_check_data(path, encoding):
    df = pd.read_csv(path, encoding=encoding)
    print("Pierwsze 5 wierszy danych:")
    print(df.head())
    print("\nSprawdzenie brakujących danych:")
    print(df.isnull().sum())
    return df


# Loading datar
try:
    train_data = load_and_check_data("../data/processed/2021_processed.csv", 'ISO-8859-2')
    test_data = load_and_check_data("../data/processed/2022_processed.csv", 'ISO-8859-2')
except UnicodeDecodeError:
    train_data = load_and_check_data("../data/processed/2021_processed.csv", 'cp1250')
    test_data = load_and_check_data("../data/processed/2022_processed.csv", 'cp1250')

# Preparing data
# todo: this should be done in etl.py or somewhere else
train_data = prepare_data(train_data)
test_data = prepare_data(test_data)

# Checking whether there is any data still missing
print("Brakujące dane po przygotowaniu (trening):")
print(train_data.isnull().sum())
print("Brakujące dane po przygotowaniu (test):")
print(test_data.isnull().sum())

# Checking data types
print("\nTypy danych w zbiorze treningowym:")
print(train_data.dtypes)

# Separating variables
X_train = train_data.drop(columns=["czy_pada"])
y_train = train_data["czy_pada"]
X_test = test_data.drop(columns=["czy_pada"])
y_test = test_data["czy_pada"]

# Building and training the model
log_model = LogisticRegression(max_iter=500)
log_model.fit(X_train, y_train)

# Predicting on test data
predictions = log_model.predict(X_test)

# Printing evaluation metrics
print(classification_report(y_test, predictions))
print(confusion_matrix(y_test, predictions))

# Saving model to a file in the model folder
dump(log_model, '../model/trained_log_model.joblib')
