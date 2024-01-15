from django.contrib.auth import get_user_model

from jagazone.config import celery_app

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    print(User.objects.count())
    return User.objects.count()
