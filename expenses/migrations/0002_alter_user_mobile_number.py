# Generated by Django 4.2.6 on 2023-10-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]