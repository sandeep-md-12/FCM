from celery import Celery

celery_app = Celery(
    "notification_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"]
)

# Force task registration
# import app.tasks.notification_tasks
