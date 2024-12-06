from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import Tenant, Payment

@receiver(post_save, sender=Tenant)
def create_initial_payments(sender, instance, created, **kwargs):
    """
    Signal to create an initial payment for the current month when a tenant is created.
    """
    first_day_of_month = date.today().replace(day=1)

    if created:
        # Create a payment for the current month
        Payment.objects.get_or_create(
            tenant=instance,
            month=first_day_of_month,
            defaults={
                'amount': instance.property.rent,
                'status': 'new'
            }
        )
