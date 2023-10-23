
from django.contrib import admin
from django.urls import path , include
from expenses import urls as expense_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('splitwise/' , include(expense_url))
]
