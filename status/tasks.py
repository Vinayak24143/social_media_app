import string
from celery import shared_task
from .models import Status
from django.utils import timezone

@shared_task
def remove_status_task(total):
    time_delta_24_hours=timezone.now()-timezone.timedelta(hours=24)
    statuses= Status.objects.filter(created_at__lt=time_delta_24_hours).delete()