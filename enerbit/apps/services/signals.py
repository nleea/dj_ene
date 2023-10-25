from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WorkOrder, Customer
from django.utils import timezone


@receiver(post_save, sender=WorkOrder)
def active_status(sender, **kwargs):
    instance = kwargs["instance"]
    customer = Customer.objects.get(pk=instance.customer_id.pk)

    if instance.status == "NEW":
        customer.start_date = timezone.now()

    elif instance.status == "DONE":

        if customer.is_active:
            customer.end_date = timezone.now()
            customer.is_active = False
        else:
            customer.is_active = True

    # customer.save()
