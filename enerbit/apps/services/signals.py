from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WorkOrder, Customer
from django.utils import timezone
import redis
import environ

env = environ.Env()


REDIS_PASSWORD: str = env("REDIS_PASSWORD")
REDIS_PORT = env("REDIS_PORT")
REDIS_HOST = env("REDIS_HOST")
REDIS_CHANNEL = env("REDIS_CHANEL")


def broker_message(work_order):
    r = redis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD, decode_responses=True
    )
    r.xadd(name=REDIS_CHANNEL, id="*", fields=work_order)


@receiver(post_save, sender=WorkOrder)
def active_status(sender, **kwargs):
    instance = kwargs["instance"]
    customer = Customer.objects.get(pk=instance.customer.pk)

    if instance.status == "NEW":
        customer.start_date = timezone.now()

    elif instance.status == "DONE":
        if customer.is_active:
            customer.end_date = timezone.now()
            customer.is_active = False
        else:
            customer.is_active = True

    customer.save()

    work_order = {
        "status": instance.status,
        "order": instance.pk,
        "customer": instance.customer.pk,
        "evenType": "change_status",
    }

    broker_message(work_order)
