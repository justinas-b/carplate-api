from celery import shared_task
import tempfile
from .models import Registration
from django.core.files import File
from icrawler.builtin import GoogleImageCrawler
import os
import glob


@shared_task
def retrieve_image_task(plate):
    """
    Retrieves photography of car and updates image field
    :param plate: Plate number to retrieve image for
    :return: None
    """

    print(f"Task has been called for {plate}")
    instance = Registration.objects.get(plate=plate)
    instance.retrieve_image = False  # Mark instance as no update required

    # Check if image is already present in cache
    cached_image = glob.glob(f"images/{instance.car_model.replace(' ', '_')}.*")
    print(f"images/{instance.car_model.replace(' ', '_')}.*")
    print(cached_image)
    if len(cached_image):
        print("Image already exists in cache")
        instance.image = cached_image.pop()
        instance.save()
    else:
        print(f"Searching internet for {instance.car_model} car model")
        with tempfile.TemporaryDirectory() as tempdir:
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

            google_crawler.crawl(keyword=instance.car_model, filters=filters, max_num=1, file_idx_offset=0)
            temp_files = os.listdir(tempdir)

            if len(temp_files):
                print("Image successfully downloaded from internet")
                temp_file_name = temp_files.pop()
                image_path = os.path.join(tempdir, temp_file_name)

                with open(image_path, "rb") as image:
                    django_file = File(image)
                    instance.image.save(name=f"{instance.car_model}.jpg", content=django_file, save=True)
            else:
                print("image not found")
                instance.image = "images/404.jpg"
                instance.save()

    print("Updating image completed")
