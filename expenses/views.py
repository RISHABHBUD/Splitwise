from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Expense, Transaction
from .serializers import UserSerializer, ExpenseSerializer, TransactionSerializer
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        expense = serializer.instance
        payer = expense.payer
        participants = expense.participants.all()
        total_participants = participants.count()

        if expense.expense_type == 'EQUAL':
            share = expense.amount / total_participants
            shares = [share] * total_participants
        elif expense.expense_type == 'EXACT':
            shares = request.data.get('shares', [])
            if sum(shares) != expense.amount:
                return Response({'error': 'Total shares do not match the total amount.'}, status=status.HTTP_400_BAD_REQUEST)
        elif expense.expense_type == 'PERCENT':
            percentages = request.data.get('percentages', [])
            if round(sum(percentages), 2) != 100:
                return Response({'error': 'Total percentages do not equal 100.'}, status=status.HTTP_400_BAD_REQUEST)
            share = (expense.amount / 100)

        expense_shares = []

        for i, participant in enumerate(participants):
            share = shares[i] if expense.expense_type == 'EXACT' else share
            share = (Decimal(percentages[i]) / 100) * expense.amount if expense.expense_type == 'PERCENT' else share

            expense_share = Transaction.objects.create(
                sender=payer,
                receiver=participant,
                amount=share,
                description=f'Expense split for {participant.name}'
            )
            expense_shares.append(expense_share)

        expense_share_serializer = TransactionSerializer(expense_shares, many=True)

        for participant in participants:
                expense = Expense.objects.get(id=expense.id)
                participant = User.objects.get(id=participant.id)

                # Calculate the amount the participant owes
                total_amount = expense.amount
                num_participants = expense.participants.count()
                share = total_amount / num_participants

                # Send email to the participant
                subject = f'Expense Notification for {expense.description}'
                message = f'Hello {participant.name},\n\n'
                message += f'You have been added to an expense by {expense.payer.name}.\n'
                message += f'You owe Rs {share:.2f} for this expense.\n\n'
                message += f'Thank you for using our expense-sharing app!'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [participant.email]
                send_mail(subject, message, from_email, recipient_list)

        return Response({'message': 'Expense split and uploaded successfully.', 'expense_shares': expense_share_serializer.data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def balances(self, request):
        users = User.objects.all()
        balances = []

        for user1 in users:
            for user2 in users:
                if user1 != user2:
                    received_amount = Transaction.objects.filter(sender=user1, receiver=user2).aggregate(total_received=Sum('amount'))['total_received'] or Decimal(0)
                    sent_amount = Transaction.objects.filter(sender=user2, receiver=user1).aggregate(total_sent=Sum('amount'))['total_sent'] or Decimal(0)
                    balance = received_amount - sent_amount

                    if balance > 0:
                        balance_str = f"{user2.name} owes {user1.name}: Rs {balance}"
                        balances.append(balance_str)
        balances.sort()
        return Response(balances, status=status.HTTP_200_OK)
