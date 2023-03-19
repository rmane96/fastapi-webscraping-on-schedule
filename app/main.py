from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table
from app import config
from app.db import get_session
from app.models import Product, ProductScrapeEvent
from app.schemas import *
from typing import List
from app.crud import *

settings = config.get_settings()


app = FastAPI()

session = None

@app.on_event("startup")
def on_startup():
    global session
    session = get_session()
    sync_table(Product)
    sync_table(ProductScrapeEvent)



@app.get("/")
def hello():
    return {
        "data":"hello world"
    }
    

@app.get("/products",response_model=List[ProductListSchema])
async def products_list_view():
    return list(Product.objects.all())



@app.post("/events/scrape")
async def create_scrape_event(data:ProductListSchema):
    product, scrape_obj = add_scrape_event(data.dict())
    return product



@app.get("/products/{asin}")
def products_detail_view(asin):
    try:
        data = dict(Product.objects.get(asin=asin))
        events = list(ProductScrapeEvent.objects().filter(asin=asin).limit(10))
        events = [ProductScrapeEventDetailSchema(**x) for x in events]
        data['events'] = events
        data['events_url'] = f"/products/{asin}/events"
        return data
    except Exception:
        data = {
            "error" : "Not Found",
            "msg" : f" '{asin}' does not exists"
        }
        return data



@app.get("/products/{asin}/events", response_model=List[ProductScrapeEventDetailSchema])
def products_scrapes_list_view(asin):
    return list(ProductScrapeEvent.objects().filter(asin=asin))




