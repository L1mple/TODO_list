from celery import Celery


def create_celery(app_name: str, broker_url: str, backend_url: str) -> Celery:
    """Factory for celery app."""
    celery_app = Celery(app_name, broker=broker_url, backend=backend_url)
    return celery_app
