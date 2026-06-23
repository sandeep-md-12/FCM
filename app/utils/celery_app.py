from celery import Celery

celery_app = Celery(
    "notification_worker",
    broker="redis://127.0.0.1:6379/0",  # Switched to explicit IP address
    backend="redis://127.0.0.1:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
    # CRITICAL: Force Celery to always send tasks to the Redis queue
    task_always_eager=False,
    task_eager_propagates=False
)

# celery_app.autodiscover_tasks(
#     ["app.tasks"]
# )

# Force task registration
import app.tasks.notification_tasks

# celery_app.conf.task_always_eager = True
