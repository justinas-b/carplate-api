from re import match

from django.forms import ModelForm, ValidationError

from .models import Registration


class RegistrationForm(ModelForm):

    class Meta:
        model = Registration
        fields = ('plate', 'owner', 'car_model')
        help_texts = {
            'plate': None,
            'owner': None,
            'car_model': None,
        }

    def clean_car_model(self):
        car_model = self.cleaned_data['car_model']

        if not match(Registration.car_and_owner_regex, car_model):
            raise ValidationError(
                "Car model must be at least two alpha-numeric words")

        return car_model

    def clean_owner(self):
        owner = self.cleaned_data['owner']

        if not match(Registration.car_and_owner_regex, owner):
            raise ValidationError(
                "Owner must be at least two alpha-numeric words")

        return owner

    def clean_plate(self):
        plate = self.cleaned_data['plate']

        if not match(Registration.car_plate_regex, plate):
            raise ValidationError(
                "Provided car plate does not match any approved models. Please refer to README file")

        return plate
