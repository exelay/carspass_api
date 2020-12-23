import uuid
import yaml
from typing import Optional

from fastapi import FastAPI
from scrapyd_api import ScrapydAPI
from pymongo import MongoClient

from settings import PROJECT_NAME, MONGO_PASSWORD


app = FastAPI()
scrapyd = ScrapydAPI()

client = MongoClient(
    f"mongodb+srv://imdb:{MONGO_PASSWORD}@carspass.mskrx.mongodb.net/Carspass?retryWrites=true&w=majority"
)
db = client['Carspass']


async def adapt_config(config: dict, site: str) -> dict:
    with open(f'conventions/{site}.yaml') as f:
        conventions = yaml.load(f, Loader=yaml.FullLoader)
    if site == 'autoru':
        v_min = int(float(config['v_min']) * 1000) if config['v_min'] else None
        v_max = int(float(config['v_max']) * 1000) if config['v_max'] else None
    else:
        v_min = config['v_min']
        v_max = config['v_max']
    return {
        'city': conventions['city'].get(config['city']),
        'transmission': conventions['transmission'].get(config['transmission']),
        'steering_w': conventions['steering_w'].get(config['steering_w']),
        'car_body': conventions['car_body'].get(config['car_body']),
        'v_min': v_min,
        'v_max': v_max,
    }


async def run_spiders(token: uuid, brand: str, model: str, sites: list, config: dict):
    for site in sites:
        site_config = await adapt_config(config, site)
        scrapyd.schedule(PROJECT_NAME, site,
                         brand=brand, model=model, token=token,
                         city=site_config['city'], radius=config['radius'],
                         transmission=site_config['transmission'], price_min=config['price_min'],
                         price_max=config['price_max'], year_min=config['year_min'], year_max=config['year_max'],
                         v_min=site_config['v_min'], v_max=site_config['v_max'],
                         steering_w=site_config['steering_w'], car_body=site_config['car_body'])


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
    results = list()
    collection = db[token]
    for elem in collection.find():
        elem.pop('_id')
        results.append(elem)
    return {'search_token': token, 'data': results}
