# Generated by Django 4.0.3 on 2022-04-05 08:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('critics', '0002_alter_ticket_description_alter_ticket_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.CharField(blank=True, max_length=8192, verbose_name='Commentaire'),
        ),
        migrations.AlterField(
            model_name='review',
            name='headline',
            field=models.CharField(max_length=128, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Note'),
        ),
    ]
