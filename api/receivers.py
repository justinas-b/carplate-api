import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Registration
from .tasks import retrieve_image_task

logger = logging.getLogger(__name__)  # Get an instance of a logger


@receiver(post_save, sender=Registration)
def registration_post_save_receiver(sender, instance, **kwargs):
    """This function is invoked after successfully completing save() operation on Registration model

    Args:
        sender: model
        instance: model instance which is being saved
    Return:
        None
    """

    logger.debug("Instance: %s", instance)
    logger.debug("Sender: %s", sender)

    if instance.retrieve_image:
        logger.info("Registering new task to retrieve car image for %s car plate", instance.plate)
        retrieve_image_task.delay(plate=instance.plate)
