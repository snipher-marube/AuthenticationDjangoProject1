# Generated by Django 4.1.2 on 2022-10-29 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_profile_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
