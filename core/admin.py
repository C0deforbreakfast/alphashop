from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 
              'phone_number', 'is_staff', 'is_superuser')
    list_display = ['first_name', 'last_name', 'email', 
                    'phone_number', 'user_wallet', 'user_membership']
    search_fields = ['first_name']
    list_select_related = ['customer']
    list_per_page = 10
    list_filter = ['customer__membership']

    def user_wallet(self, user):
        return user.customer.wallet
    
    def user_membership(self, user):
        return user.customer.membership

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request) \
            .prefetch_related('customer')


{
    "phone_number": "09000000000",
    "first_name": "Sina",
    "last_name": "Khare",
    "email": "as@domain.com",
    "password": "IloveDjango123@",
    "confirm_password": "IloveDjango123@"
}

