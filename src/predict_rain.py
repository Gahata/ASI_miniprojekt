import os
from joblib import load
import pandas as pd


def predict(maksymalna_temperatura, minimalna_temperatura, srednia_temperatura, temperatura_minimalna_przy_gruncie,
            suma_dobowa_opadow, wysokosc_pokrywy_snieznej):
    loaded_model = load('../model/trained_log_model.joblib')
    dane = {
        'max_temp_dobowa': [maksymalna_temperatura],
        'min_temp_dobowa': [minimalna_temperatura],
        'srednia_temp_dobowa': [srednia_temperatura],
        'min_temp_przy_gruncie': [temperatura_minimalna_przy_gruncie],
        'suma_dobowa_opadow': [suma_dobowa_opadow],
        'wysokosc_pokrywy_snieznej': [wysokosc_pokrywy_snieznej]
    }
    df = pd.DataFrame(dane)
    prediction = loaded_model.predict(df)
    return prediction[0]
