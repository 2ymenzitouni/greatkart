from django.contrib import admin
from .models import Account
# Register your models here.

from django.contrib.auth.admin import UserAdmin
class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)

    list_filter =()
    filter_horizontal=()
    fieldsets = ()
admin.site.register(Account,AccountAdmin)