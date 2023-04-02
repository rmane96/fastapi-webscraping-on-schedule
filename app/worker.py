from celery import Celery
from celery.signals import beat_init, worker_process_init
from app.config import get_settings
from app import db, models, schemas, scraper, crud
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from celery.schedules import crontab

celery_app = Celery(__name__)
settings = get_settings()

REDIS_URL = settings.redis_url
celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL

Product = models.Product
ProductScrapeEvent = models.ProductScrapeEvent


def celery_on_startup(*args, **kwargs):
    if connection.cluster is not None:
        connection.cluster.shutdown()
    if connection.session is not None:
        connection.session.shutdown()    ## run sessions only once
    cluster = db.get_cluster()
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    sync_table(Product)
    sync_table(ProductScrapeEvent)


beat_init.connect(celery_on_startup)
worker_process_init.connect(celery_on_startup)


@celery_app.on_after_configure.connect  # after configure means run on after init and connection of db
def setup_periodic_tasks(sender,*args,**kwargs):
    sender.add_periodic_task(
        crontab(minute="*/5"),    #scrape every 5 minutes
        scrape_products.s(), 
        )  
    
    
# @celery_app.task
# def random_task(name):
#     print(f'helloo {name}')
    


@celery_app.task
def list_products():
    q = Product.objects().all().values_list("asin", flat=True)
    print(list(q))


@celery_app.task
def scrape_asin(asin):
    s = scraper.Scraper(asin=asin, endless_scroll=True)
    dataset =  s.scrape()
    try:
        validated_data = schemas.ProductListSchema(**dataset)
    except: 
        validated_data = None
    if validated_data is not None:
        product , _ = crud.add_scrape_event(validated_data.dict())
        return asin, True
    return asin, False


@celery_app.task
def scrape_products():
    print("Scraping.......")
    q = Product.objects().all().values_list("asin", flat=True)
    for asin in q:
        scrape_asin.delay(asin)    
    
    

