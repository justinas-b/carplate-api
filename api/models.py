from django.db import models
from django.core.validators import RegexValidator
from Models.CICharField import CICharField

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
    plate = CICharField(max_length=6, blank=False, unique=True, validators=[RegexValidator(regex=car_plate_regex)])
    owner = models.CharField(max_length=200, blank=False, unique=False, validators=[RegexValidator(regex=r'^\w+$')])
    car_model = models.CharField(max_length=200, blank=False, unique=False, validators=[RegexValidator(regex=r'^\w+$')])
    # TODO: Add photo field

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.plate

    def save(self, *args, **kwargs):
        self.plate = self.plate.upper()
        self.owner = self.owner.title()
        super(Registration, self).save(*args, **kwargs)
