from django.db import models
from django.contrib.auth.models import User
# this is a core python tool, not from django
from datetime import datetime, timedelta

# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)

    TYPE_CHOICES = [
        ('book', "Book"),
        ('magazine', "Magazine"),
    ]
    item_type = models.CharField(
        max_length=100, choices=TYPE_CHOICES, default='book')

    def __str__(self):
        return f"{self.title} - {self.author}"


class ItemLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    loaned_timestamp = models.DateTimeField(auto_now_add=True)
    returned_timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.item.title} - {self.user.username}"

    def daysLeft(self):
        date_to_return = self.loaned_timestamp + timedelta(days=30)
        days_left = (date_to_return - self.loaned_timestamp).days
        return days_left

    def is_available(self):
        return True if returned_timestamp != NULL else False
