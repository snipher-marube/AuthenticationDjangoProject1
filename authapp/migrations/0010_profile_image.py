# Generated by Django 4.1.2 on 2022-10-31 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='images/img2.jpeg', upload_to='profile_pics'),
        ),
    ]