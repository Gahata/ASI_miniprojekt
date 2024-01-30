from pydantic import BaseModel


class WeatherCreate(BaseModel):
    max_temp_dobowa: float
    min_temp_dobowa: float
    srednia_temp_dobowa: float
    min_temp_przy_gruncie: float
    suma_dobowa_opadow: float
    wysokosc_pokrywy_snieznej: float


class Weather(WeatherCreate):
    id: int
