from django.contrib import admin
from .models import Order,Table,Reservation,Inventory,MenuItem

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Inventory)