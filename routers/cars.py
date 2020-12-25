import uuid
from typing import Optional

from fastapi import APIRouter, Query

from utils import run_spiders, spiders_finished
from settings import DB


router = APIRouter()


@router.post('/cars/startSearch', tags=['cars'])
async def start_search(
    sites: str,
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
):
    """
    A **POST** method that starts searching process and return response with JSON
    that contain status and unique search **token**.
    This **token** will be needed to get search results in the **getResults** method.
    """
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


@router.get('/cars/getResults', tags=['cars'])
async def get_results(token: str):
    """
    A GET method that returns JSON response containing search results.
    """
    while True:
        if await spiders_finished(token):
            break
    results = list()
    collection = DB[token]
    for elem in collection.find():
        elem.pop('_id')
        results.append(elem)
    return {'search_token': token, 'data': results}
