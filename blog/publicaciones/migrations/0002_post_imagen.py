# Generated by Django 3.2.9 on 2021-12-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='imagen',
            field=models.FileField(default=' ', upload_to='imagenes_blog/publicaciones/'),
        ),
    ]