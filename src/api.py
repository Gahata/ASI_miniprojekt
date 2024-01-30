from fastapi import FastAPI
import predict_rain

app = FastAPI()


@app.get("/")
async def read_root():
    return {"This is an API for rainy weather prediction"}


@app.get('/predict')
async def predict(
        max_temp_dobowa: float,
        min_temp_dobowa: float,
        srednia_temp_dobowa: float,
        min_temp_przy_gruncie: float,
        suma_dobowa_opadow: float,
        wysokosc_pokrywy_snieznej: float
):
    prediction = await predict_rain.predict(max_temp_dobowa, min_temp_dobowa, srednia_temp_dobowa, min_temp_przy_gruncie,
                                      suma_dobowa_opadow, wysokosc_pokrywy_snieznej)
    response = {
        'Logistic regression prediction ': prediction
    }
    return response
