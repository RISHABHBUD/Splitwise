from django.contrib import admin
from .models import User , Expense , Transaction

admin.site.register(User)
admin.site.register(Expense)
admin.site.register(Transaction)


