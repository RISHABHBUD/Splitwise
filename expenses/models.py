from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15 , unique=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=10, choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent')])
    split_percentages = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='expenses', blank=True)

    def __str__(self):
        return str(self.payer)


class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

