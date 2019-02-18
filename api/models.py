from django.db import models
from django.core.validators import RegexValidator
from Models.CICharField import CICharField
import logging
from django.contrib import admin

logger = logging.getLogger(__name__)  # Get an instance of a logger


# Create your models here.
class Registration(models.Model):
    """
    Car plate registration model
    """

    # RegEx for validating car plate pattern
    car_plate_regex = r'^([a-zA-Z]{2,3}\d{3}|' \
                      r'[a-zA-Z]{2}\d{2}|' \
                      r'\d{3}[a-zA-Z]{2}|' \
                      r'\d{2}[a-zA-Z]{3}|' \
                      r'\d{1}[a-zA-Z]{4,5}|' \
                      r'\d{4}[a-zA-Z]{1,2}|' \
                      r'[THP]\d{5}|\d{5,6}|' \
                      r'\d{4}H|P\d{4}|' \
                      r'E[a-zA-Z]\d{4})$'

    created = models.DateTimeField(auto_now_add=True)
    plate = CICharField(max_length=6, blank=False, unique=True, validators=[RegexValidator(regex=car_plate_regex)],
                        help_text="Car plate number (as per Lithuanian standards)")
    owner = models.CharField(max_length=200, blank=False, help_text="Owner's full name (Name and Surname)",
                             unique=False, validators=[RegexValidator(regex=r'^(\w+\s*)+$')])
    car_model = models.CharField(max_length=200, blank=False, help_text="Car make and model",
                                 unique=False, validators=[RegexValidator(regex=r'^(\w+\s*)+$')])
    # image = models.ImageField(storage=fs, blank=True, unique=False)
    image = models.ImageField(upload_to='images', blank=True, unique=False,
                              help_text="Car model's image", editable=False)
    retrieve_image = models.BooleanField(default=True, help_text="Specifies if car image should be retrieved",
                                         editable=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.plate

    # Override save method in order to:
    # - capitalize plate number
    # - set title case for owner field
    # - capitalize car model
    # - and verify if car image shouuld be retrieved
    def save(self, *args, **kwargs):
        # Check if car model has changed and if so, mark object as Update Required
        if self.pk is not None and self.retrieve_image is False:
            original = Registration.objects.get(pk=self.pk)  # Compare current
            if original.car_model != self.car_model:  # Compare new and old values of car model
                logger.info(f"Car model changed from '{original.car_model}' to '{self.car_model}'")
                self.retrieve_image = True

        self.plate = self.plate.upper()
        self.car_model = self.car_model.upper()
        self.owner = self.owner.title()
        super(Registration, self).save(*args, **kwargs)


class RegistrationAdmin(admin.ModelAdmin):
    readonly_fields = ('image',)
