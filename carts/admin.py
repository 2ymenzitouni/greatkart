from django.contrib import admin
from .models import Cart , CartItem , Variation
# Register your models here.
admin.site.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('product','user','cart')

admin.site.register(CartItem ,CartAdmin)
