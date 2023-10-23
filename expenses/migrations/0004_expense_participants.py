# Generated by Django 4.2.6 on 2023-10-22 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_remove_expense_participants_expenseshare'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='expenses', to='expenses.user'),
        ),
    ]