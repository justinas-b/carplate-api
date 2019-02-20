import glob
import logging
import os
import tempfile

from celery import shared_task
from django.core.files import File
from icrawler.builtin import GoogleImageCrawler

from .models import Registration

logger = logging.getLogger(__name__)  # Get an instance of a logger


def get_image_from_cache(car_model: str) -> str:
    """Checks if provided car model has image stored in local cache.
    If image is found it will return path to the image, otherwise None is returned

    Args:
        car_model (str): car model

    Returns:
        str: Path to the cached image. If image is not found, function returns None
    """

    logger.debug("Checking image cache for %s", car_model)
    files = glob.glob(f"images/{car_model.replace(' ', '_')}.*")
    if files:
        image = files.pop()
        logger.debug("Image found in cache: %s", image)
    else:
        image = None
        logger.debug("%s image not present in cache", car_model)

    return image


def download_image(car_model: str) -> str:
    """Downloads image of provided car model from internet.
    If image is found it will return path to the image, otherwise None is returned

    Args:
        car_model (str): car model

    Returns:
        str: Path to downloaded image. If image is not found, function returns None
    """
    logger.debug("Downloading %s image from internet", car_model)
    # tempdir = tempfile.TemporaryDirectory().name
    tempdir = tempfile.mkdtemp()

    google_crawler = GoogleImageCrawler(
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=1,
        storage={'root_dir': tempdir})

    filters = dict(
        size='large',
        color='orange',
        license='commercial,modify',
        type='photo'
    )
    google_crawler.crawl(keyword=car_model, filters=filters, max_num=1, file_idx_offset=0)
    temp_files = os.listdir(tempdir)

    if temp_files:
        image_name = temp_files.pop()
        image_path = os.path.join(tempdir, image_name)
        logger.debug("Image successfully downloaded from internet (%s)", image_path)

    else:
        logger.debug("Image not found")
        image_path = None

    return image_path


@shared_task
def retrieve_image_task(plate: str) -> None:
    """Retrieves photography of car and updates image field

    Args:
        plate: Plate number to retrieve image for
    Return:
        None
    """

    logger.info("Task has been called for %s", plate)
    instance = Registration.objects.get(plate=plate)
    instance.retrieve_image = False  # Mark instance as no update required

    # Check if image is already present in cache
    cached = get_image_from_cache(car_model=instance.car_model)
    if cached:
        logger.info("Saving image from local cache")
        instance.image = cached
        instance.save()
    # Otherwise try downloading image from internet
    else:
        logger.info("Searching internet for %s car model", instance.car_model)
        image = download_image(car_model=instance.car_model)

        if image:  # If image was successfully downloaded
            with open(image, "rb") as image:
                django_file = File(image)
                instance.image.save(name=f"{instance.car_model}.jpg", content=django_file, save=True)
        else:  # If failed to download image, apply default one
            logger.info("Image not found, defaulting to 404")
            instance.image = "images/404.jpg"
            instance.save()

    logger.info("Updating image completed")
