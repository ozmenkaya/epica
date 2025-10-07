from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Ticket)
def ticket_created_notify_suppliers(sender, instance: Ticket, created: bool, **kwargs):
    if not created:
        return
    # Notify suppliers assigned by rules (fallback to category.suppliers). Stub: logs only.
    if instance.category_id:
        try:
            suppliers = instance.assigned_suppliers.all()
        except Exception:
            suppliers = instance.category.suppliers.all()
        for sup in suppliers:
            logger.info(
                "Notify supplier %s (id=%s) about new ticket #%s in org %s",
                sup.name,
                sup.id,
                instance.id,
                instance.organization_id,
            )
