from app.db import get_session
import copy
from app.models import Product, ProductScrapeEvent
from cassandra.cqlengine.management import sync_table
import uuid

session = get_session()

sync_table(Product)
sync_table(ProductScrapeEvent)


def create_entry(data:dict):
    return Product.create(**data)

def create_scrape_event(data:dict):
    data['uuid'] = uuid.uuid1()
    return ProductScrapeEvent.create(**data)

def add_scrape_event(data:dict,fresh=False):    #creates uuid id field not entered error if not used deep copy
    if fresh:
        data = copy.deepcopy(data)
    product = create_entry(data)
    scrape_obj = create_scrape_event(data)
    return product, scrape_obj




data = {"asin": "EXAMPLE","title": "phone","price_str":"16000"}

