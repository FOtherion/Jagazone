# Generated by Django 4.2.7 on 2023-11-21 21:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usersprofile",
            name="archived",
            field=models.DateTimeField(blank=True),
        ),
    ]
