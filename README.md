docker run --restart always -d -p 6380:6380 redis 


/// celery start worker process with log info
celery --app app.worker.celery_app worker -l INFO


/// celery start beat (scheduling only) with log
celery --app app.worker.celery_app beat -l INFO

/// celery start beat scheduling and worker process with log
celery --app app.worker.celery_app worker --beat -s <name> -l INFO


docker run -it --rm -p 6380:6380 redis --port 6380












