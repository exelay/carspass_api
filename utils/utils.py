import yaml

from scrapyd_api import ScrapydAPI


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
