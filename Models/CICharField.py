# http://concisecoder.io/2018/10/27/case-insensitive-fields-in-django-models/

from django.db import models
from Models.CaseInsensitiveFieldMixin import CaseInsensitiveFieldMixin


class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass
