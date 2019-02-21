import json

from django.test import Client, TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from ..models import Registration
from ..serializers import RegistrationSerializer
from ..forms import RegistrationForm


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

    def test_valid_form(self):
        registration = Registration.objects.create(plate='ZXY123', owner='john doe', car_model='Demo Car')
        data = {'plate': registration.plate[1:], 'owner': registration.owner, 'car_model': registration.car_model, }
        form = RegistrationForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form_duplicate_plate(self):
        registration = Registration.objects.create(plate='ZXY123', owner='john doe', car_model='Demo Car')
        data = {'plate': registration.plate, 'owner': registration.owner, 'car_model': registration.car_model, }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_plate_number(self):
        form = RegistrationForm({'plate': 'AB', 'owner': 'john doe', 'car_model': 'Demo Car'})
        self.assertFalse(form.is_valid())

    def test_invalid_name_and_model_in_form(self):
        form = RegistrationForm(data=self.invalid_payload)
        self.assertFalse(form.is_valid())
