from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import MenuItem, Table, Order, Reservation, Inventory
from .serializers import (MenuItemSerializer, OrderSerializer, TableSerializer, ReservationSerializer, InventorySerializer)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class AvailableMenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        available_ids = Inventory.objects.filter(amount__gt=0).values_list('item_id', flat=True)
        return MenuItem.objects.filter(available=True, id__in=available_ids)

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class AvailableTableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Table.objects.filter(is_available=True)
    serializer_class = TableSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        reservation = serializer.save()
        table = reservation.table
        table.is_available = False
        table.save()


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


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
