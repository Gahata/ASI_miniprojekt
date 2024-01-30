import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump

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
