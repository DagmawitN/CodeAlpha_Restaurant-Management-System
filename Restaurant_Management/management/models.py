from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    name = models.CharField(max_length=124)
    price = models.FloatField()
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    seats = models.IntegerField(default=4)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(MenuItem, related_name='orders')
    time = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - Table {self.table.table_number} on {self.date} at {self.time}"


class Inventory(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='inventory')
    amount = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.amount} in stock"
