from django.db.utils import IntegrityError
from django.test import Client, TestCase

from ..models import Registration
from ..tasks import get_image_from_cache, retrieve_image_task


class ModelTests(TestCase):
    """ Test module for Registration model """

    def setUp(self):
        """Prepare test environment."""
        self.OWNER = "john doe"
        self.CAR = "super car"
        self.PLATE = "abc123"
        self.INVALID_TEXT = "OnlyOneWord"

        self.client = Client()

        self.reg_first = Registration.objects.create(plate=self.PLATE, owner=self.OWNER, car_model=self.CAR)
        self.reg_second = Registration.objects.create(plate=self.PLATE[::-1], owner=self.OWNER, car_model=self.CAR)
        self.reg_third = Registration.objects.create(plate=self.PLATE[1:6], owner=self.OWNER[::-1],
                                                     car_model=self.CAR[::-1])

        self.valid_payload = {
            'plate': 'ABC234',
            'car_model': 'test model',
            'owner': 'John Doe'
        }

        self.invalid_payload = {
            'plate': 'ABC234',
            'car_model': 'testmodel',
            'owner': 'JohnDoe',
        }

    # Cleanup once tests are completed.
    def tearDown(self):
        pass

    def test_car_name_is_upper_case(self):
        """Test to check car name is changed to upper case upon the save operation."""
        registration = Registration.objects.get(plate=self.PLATE)
        self.assertEqual(registration.car_model, self.CAR.upper())

    def test_car_plate_is_upper_case(self):
        """Test to check car plate is changed to upper case upon the save operation."""
        registration = Registration.objects.get(plate=self.PLATE)
        self.assertEqual(registration.plate, self.PLATE.upper())

    def test_owner_name_has_title_case(self):
        """Test to check car owner's name is changed to title case upon the save operation."""
        registration = Registration.objects.get(plate=self.PLATE)
        self.assertEqual(registration.owner, self.OWNER.title())

    def test_duplicate_car_plate_throws_exception(self):
        """Test to ensure no new record can be created with existing car plate."""
        with self.assertRaises(IntegrityError):
            Registration.objects.create(plate=self.PLATE, owner=self.OWNER, car_model=self.CAR)

    def test_image_caching(self):
        """Test to verify image can be retrieved from cache if it exists."""

        non_cached_image = get_image_from_cache(car_model=self.CAR)
        cached_image = get_image_from_cache(car_model='404')
        self.assertEqual(non_cached_image, None)
        self.assertEqual(cached_image, 'images/404.jpg')

    def test_image_download(self):
        """Test to verify image can be downloaded from internet."""
        retrieve_image_task(plate=self.PLATE)
        registration = Registration.objects.get(plate=self.PLATE)
        self.assertEqual(registration.image.path, f"/code/images/{registration.car_model.replace(' ', '_')}.jpg")

