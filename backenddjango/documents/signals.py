from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Fee, Repayment, Ledger


@receiver(post_save, sender=Fee)
def create_ledger_on_fee_save(sender, instance, created, **kwargs):
    """Signal handler to create ledger entries when a fee is created or paid"""
    if created:
        Ledger.objects.create(
            application=instance.application,
            transaction_type='fee_created',
            amount=instance.amount,
            description=f"Fee created: {instance.get_fee_type_display()}",
            transaction_date=timezone.now(),
            related_fee=instance,
            created_by=instance.created_by
        )
    elif instance.paid_date and not Ledger.objects.filter(
        related_fee=instance,
        transaction_type='fee_paid'
    ).exists():
        Ledger.objects.create(
            application=instance.application,
            transaction_type='fee_paid',
            amount=instance.amount,
            description=f"Fee paid: {instance.get_fee_type_display()}",
            transaction_date=instance.paid_date,
            related_fee=instance,
            created_by=instance.created_by
        )


@receiver(post_save, sender=Repayment)
def create_ledger_on_repayment_save(sender, instance, created, **kwargs):
    """Signal handler to create ledger entries when a repayment is created or paid"""
    if created:
        Ledger.objects.create(
            application=instance.application,
            transaction_type='repayment_scheduled',
            amount=instance.amount,
            description=f"Repayment scheduled for {instance.due_date}",
            transaction_date=timezone.now(),
            related_repayment=instance,
            created_by=instance.created_by
        )
    elif instance.paid_date and not Ledger.objects.filter(
        related_repayment=instance,
        transaction_type='repayment_received'
    ).exists():
        Ledger.objects.create(
            application=instance.application,
            transaction_type='repayment_received',
            amount=instance.amount,
            description=f"Repayment received for {instance.due_date}",
            transaction_date=instance.paid_date,
            related_repayment=instance,
            created_by=instance.created_by
        )
