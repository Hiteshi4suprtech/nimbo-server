# Generated by Django 5.0.6 on 2024-07-11 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_symptoms', '0002_symptoms_login_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Symptoms',
        ),
    ]
