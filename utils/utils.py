import uuid
import yaml
from typing import Union
from scrapyd_api import ScrapydAPI

from settings import PROJECT_NAME

scrapyd = ScrapydAPI()
JOBS = dict()


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
        'city': conventions.get('city').get(config['city']),
        'transmission': conventions.get('transmission').get(config['transmission']),
        'steering_w': conventions.get('steering_w').get(config['steering_w']),
        'car_body': conventions.get('car_body').get(config['car_body']),
        'v_min': v_min,
        'v_max': v_max,
        'vendor': conventions.get('vendor').get(config['vendor']),
    }


async def run_spiders(
        token: uuid,
        brand: Union[str, None],
        model: Union[str, None],
        sites: list,
        config: dict
) -> None:
    JOBS[token] = list()
    for site in sites:
        site_config = await adapt_config(config, site)
        job = scrapyd.schedule(PROJECT_NAME, site,
                               brand=brand, model=model, token=token,
                               city=site_config['city'], radius=config['radius'],
                               transmission=site_config['transmission'], price_min=config['price_min'],
                               price_max=config['price_max'], year_min=config['year_min'], year_max=config['year_max'],
                               v_min=site_config['v_min'], v_max=site_config['v_max'],
                               steering_w=site_config['steering_w'], car_body=site_config['car_body'],
                               vendor=site_config['vendor'], latest_ads=config['latest_ads'])
        JOBS[token].append(job)


async def spiders_finished(token: uuid) -> bool:
    finished_jobs = [job['id'] for job in scrapyd.list_jobs(PROJECT_NAME)['finished']]
    try:
        jobs = JOBS[token]

        for job in jobs:
            if job not in finished_jobs:
                return False

        JOBS.pop(token)
        return True
    except KeyError:
        return True
