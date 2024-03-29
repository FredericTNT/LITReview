# Generated by Django 4.0.3 on 2022-03-31 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('critics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True, max_length=2048, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name="Photo du livre ou de l'article"),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Titre'),
        ),
    ]
