import uuid

from fastapi import FastAPI
from typing import Optional


app = FastAPI()


async def run_spiders(token: uuid, brand: str, model: str, sites: list, config: dict):
    spiders = {}
    for site in sites:
        spider = spiders[site]


@app.post('/startSearch')
async def start_search(
    brand: str,
    model: str,
    sites: str,
    city: Optional[str] = 'spb',
    radius: Optional[int] = None,
    transmission: Optional[str] = None,
    price_min: Optional[int] = None,
    price_max: Optional[int] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    v_min: Optional[float] = None,
    v_max: Optional[float] = None,
    steering_w: Optional[str] = None,
    car_body: Optional[str] = None,
):
    token = uuid.uuid1().hex
    config = {
        'city': city,
        'radius': radius,
        'transmission': transmission,
        'price_min': price_min,
        'price_max': price_max,
        'year_min': year_min,
        'year_max': year_max,
        'v_min': v_min,
        'v_max': v_max,
        'steering_w': steering_w,
        'car_body': car_body,
    }
    sites = sites.split(',')
    await run_spiders(token, brand, model, sites, config)
    return {'search_token': token}


@app.get('/getResults')
async def get_results(token: str):
    return {'search_token': token}