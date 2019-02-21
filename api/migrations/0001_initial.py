# Generated by Django 2.1.7 on 2019-02-21 21:10

import Models.CICharField
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('plate', Models.CICharField.CICharField(help_text='Car plate number (as per Lithuanian standards)', max_length=6, unique=True, validators=[django.core.validators.RegexValidator(regex='^([a-zA-Z]{2,3}\\d{3}|[a-zA-Z]{2}\\d{2}|\\d{3}[a-zA-Z]{2}|\\d{2}[a-zA-Z]{3}|\\d{1}[a-zA-Z]{4,5}|\\d{4}[a-zA-Z]{1,2}|[THP]\\d{5}|\\d{5,6}|\\d{4}H|P\\d{4}|E[a-zA-Z]\\d{4})$')])),
                ('owner', models.CharField(help_text="Owner's full name (Name and Surname)", max_length=200, validators=[django.core.validators.RegexValidator(regex='^\\w+\\s+(\\w+\\s*)+$')])),
                ('car_model', models.CharField(help_text='Car make and model', max_length=200, validators=[django.core.validators.RegexValidator(regex='^\\w+\\s+(\\w+\\s*)+$')])),
                ('image', models.ImageField(blank=True, editable=False, help_text="Car model's image", upload_to='images')),
                ('retrieve_image', models.BooleanField(default=True, editable=False, help_text='Specifies if car image should be retrieved')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
