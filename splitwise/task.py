# tasks.py
from celery import shared_task
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from expenses.models import User, Transaction
from django.db.models import Sum

@shared_task
def send_weekly_balance_reminders():
    users = User.objects.all()

    for user in users:
        balance = Decimal(0)

        received_amount = Transaction.objects.filter(receiver=user).aggregate(total_received=Sum('amount'))['total_received'] or Decimal(0)
        sent_amount = Transaction.objects.filter(sender=user).aggregate(total_sent=Sum('amount'))['total_sent'] or Decimal(0)
        balance = received_amount - sent_amount

        if balance != 0:
            subject = 'Weekly Balance Reminder'
            message = f'Hello {user.name},\n\n'
            message += f'Your balance with other users is Rs {balance:.2f}.\n'
            message += f'Please settle any pending balances.\n\n'
            message += 'Thank you for using our expense-sharing app!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)
