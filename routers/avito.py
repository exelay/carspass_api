import uuid
from typing import Optional
from time import sleep

from fastapi import APIRouter, Query
from utils.utils import run_spider

from settings import DB, PROJECT_NAME
from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI()

router = APIRouter()


@router.get('/avito/startSearch', tags=['avito'])
async def start_search(
    brand: Optional[str] = Query(None, title='Car brand'),
    model: Optional[str] = Query(None, title='Car model'),
    city: Optional[str] = Query('spb', title='City of search'),
    radius: Optional[int] = Query(100, title='Search radius'),
    transmission: Optional[str] = Query(None, title='Type of transmission'),
    price_min: Optional[int] = Query(None, title='Minimum price'),
    price_max: Optional[int] = Query(None, title='Maximum price'),
    year_min: Optional[int] = Query(None, title='Minimum year'),
    year_max: Optional[int] = Query(None, title='Maximum year'),
    v_min: Optional[float] = Query(None, title='Minimum engine capacity'),
    v_max: Optional[float] = Query(None, title='Maximum engine capacity'),
    steering_w: Optional[str] = Query(None, title='Steering wheel position'),
    car_body: Optional[str] = Query(None, title='Car body'),
    vendor: Optional[str] = Query(None, title='Vendor'),
    latest_ads: Optional[str] = Query(None, title='Latest ads in 24 or 72 hours')
):
    """
    A **POST** method that starts avito searching process and return response with JSON
    that contain status and unique search **token**.
    This **token** will be needed to get search results in the **getResults** method.
    """
    site = 'avito'
    token = uuid.uuid1().hex
    results = list()
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
        'vendor': vendor,
        'latest_ads': latest_ads,
    }
    job = await run_spider(token, brand, model, site, config)
    print(job)
    while True:
        sleep(1)
        finished_jobs = [job['id'] for job in scrapyd.list_jobs(PROJECT_NAME)['finished']]
        print(finished_jobs)
        if job in finished_jobs:
            break
    collection = DB[token]
    for elem in collection.find():
        elem.pop('_id')
        results.append(elem)
    return {'search_token': token, 'data': results}
