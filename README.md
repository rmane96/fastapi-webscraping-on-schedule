docker run --restart always -d -p 6380:6380 redis 


/// celery startup with log info
celery --app app.worker.celery_app worker -l INFO


docker run -it --rm -p 6380:6380 redis --port 6380