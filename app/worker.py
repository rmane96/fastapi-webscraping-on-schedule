from celery import Celery
from app.config import get_settings


celery_app = Celery(__name__)
settings = get_settings()
REDIS_URL = settings.redis_url


celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL


@celery_app.task
def random_task(name):
    print(f"Who throws a shoe: {name}")
    
    