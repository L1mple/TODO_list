from celery import Celery


def create_celery(app_name: str, broker_url: str, backend_url: str) -> Celery:
    """Factory for celery app."""
    celery_app = Celery(app_name, broker=broker_url, backend=backend_url)
    return celery_app


celeryyy = create_celery(
    "tasks",
    broker_url="pyamqp://admin:pa55w0rd@rabbitmq:5672/",
    backend_url="pyamqp://admin:pa55w0rd@rabbitmq:5672/",
)
