import json

from django.test import Client, TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from ..models import Registration
from ..serializers import RegistrationSerializer


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

    def test_get_all_registrations(self):
        """Test to check if all objects are available through API."""
        response = self.client.get(reverse('registration-list'))  # get API response
        registrations = Registration.objects.all()  # get data from db
        serializer = RegistrationSerializer(registrations, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_registration(self):
        """Test to check object details are the same in API."""
        response = self.client.get(reverse('registration-detail', kwargs={'pk': self.reg_first.pk}))
        registration = Registration.objects.get(pk=self.reg_first.pk)
        serializer = RegistrationSerializer(registration)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_registration(self):
        """Test 404 is returned when requesting non-existing object."""
        response = self.client.get(reverse('registration-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_registration(self):
        """Test new object can be created with valid data."""
        response = self.client.post(
            reverse('registration-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_registration(self):
        """Test new object can not be created with invalid data."""
        response = self.client.post(
            reverse('registration-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_registration(self):
        """Test to verify object can be updated with valid data."""
        response = self.client.put(
            reverse('registration-detail', kwargs={'pk': self.reg_first.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_registration(self):
        """Test to verify object can not be updated with invalid data."""
        response = self.client.put(
            reverse('registration-detail', kwargs={'pk': self.reg_first.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_registration(self):
        """Test to verify object can be deleted."""
        response = self.client.delete(
            reverse('registration-detail', kwargs={'pk': self.reg_first.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_registration(self):
        """Test to verify non-existing object can not be deleted."""
        response = self.client.delete(
            reverse('registration-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_invalid_owner(self):
        """Test to verify that object can not be created using invalid owner name."""
        payload = self.valid_payload
        payload['owner'] = self.INVALID_TEXT

        response = self.client.post(
            reverse('registration-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_car_model(self):
        """Test to verify that object can not be created using invalid car name."""
        payload = self.valid_payload
        payload['car_model'] = self.INVALID_TEXT

        response = self.client.post(
            reverse('registration-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_plate(self):
        """Test to verify that object can not be created using invalid car plate."""
        payload = self.valid_payload
        payload['plate'] = self.INVALID_TEXT

        response = self.client.post(
            reverse('registration-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_readonly_fields_are_not_modified(self):
        """Test to verify that read-only fields are not modifiable."""
        payload = self.valid_payload
        payload['image'] = self.INVALID_TEXT
        payload['retrieve_image'] = "False"

        response = self.client.post(
            reverse('registration-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        registration = Registration.objects.get(plate=payload['plate'])
        self.assertEqual(registration.image, "")
        self.assertEqual(registration.retrieve_image, True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_filtering_by_owner(self):
        """Test to verify filtering by owner's name is working fine."""
        response = self.client.get(
            reverse('registration-list'),
            {"owner": self.OWNER.title()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_registration_filtering_by_plate(self):
        """Test to verify filtering by plate is working fine."""
        response = self.client.get(
            reverse('registration-list'),
            {"plate": self.PLATE.upper()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_registration_search(self):
        """Test to verify search by plate is working fine."""

        response = self.client.get(
            reverse('registration-list'),
            {"search": self.PLATE.upper()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_registration_can_be_accessed_by_plate(self):
        """Test to check object details are the same in API when using plate in URL."""
        response = self.client.get(reverse('registration-detail-find', kwargs={'plate': self.reg_first.plate}))
        registration = Registration.objects.get(pk=self.reg_first.pk)
        serializer = RegistrationSerializer(registration)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
