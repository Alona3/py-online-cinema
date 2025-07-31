from online_cinema.tasks.email_tasks import celery

celery.autodiscover_tasks(["online_cinema.tasks"])

celery.worker_main()
