from .tasks import retrieve_image_task
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Registration
import logging

logger = logging.getLogger(__name__)  # Get an instance of a logger


@receiver(post_save, sender=Registration)
def registration_post_save_receiver(sender, instance, **kwargs):
    """
    This function is invoked after successfully completing save() operation on Registration model
    :param sender: model
    :param instance: model instance which is being saved
    :param kwargs: kwargs
    :return: None
    """
    logger.debug(f"Sender: {sender}")  # TODO: Remove this message
    logger.debug(f"Instance: {instance}")  # TODO: Remove this message
    if instance.retrieve_image:
        logger.info(f"Registering new task to retrieve car image for {instance.plate} car plate")
        retrieve_image_task.delay(plate=instance.plate)  # TODO: check delay() fingerprint
