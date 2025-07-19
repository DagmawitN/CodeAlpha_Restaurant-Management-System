from datetime import date, datetime
from django.db.models import Sum
from django.db import models
from rest_framework import viewsets, status, serializers
from rest_framework.exceptions import ValidationError

from .models import MenuItem, Table, Order, Reservation, Inventory
from .serializers import (
    MenuItemSerializer, OrderSerializer, TableSerializer,
    InventorySerializer
)


# ---------------- MENU ITEMS ----------------
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        for item in MenuItem.objects.all():
            total = Inventory.objects.filter(item=item).aggregate(total=Sum('amount'))['total'] or 0
            item.available = total > 0
            item.save()
        return MenuItem.objects.all()

# ---------------- TABLES ----------------
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


# ---------------- RESERVATIONS ----------------
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Reservation date cannot be in the past.")
        return value

    def validate(self, data):
        reservation_date = data.get('date')
        reservation_time = data.get('time')

        if reservation_date == date.today():
            now = datetime.now().time()
            if reservation_time <= now:
                raise serializers.ValidationError("Reservation time must be in the future.")
        return data


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        reservation = serializer.save()
        table = reservation.table
        table.is_available = False
        table.save()


# ---------------- ORDERS ----------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        for item in order.items.all():
            try:
                inventory = Inventory.objects.get(item=item)

                if inventory.amount <= 0:
                    raise ValidationError(f"{item.name} is out of stock.")

                inventory.amount -= 1
                inventory.save()

                if inventory.amount == 0:
                    item.available = False
                    item.save()

            except Inventory.DoesNotExist:
                raise ValidationError(f"{item.name} is not in inventory.")


# ---------------- INVENTORY ----------------
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def perform_update(self, serializer):
        inventory = serializer.save()
        item = inventory.item

        total_amount = Inventory.objects.filter(item=item).aggregate(total=Sum('amount'))['total'] or 0
        item.available = total_amount > 0
        item.save()
