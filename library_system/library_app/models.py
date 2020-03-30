from django.db import models
from django.contrib.auth.models import User
# this is a core python tool, not from django
from datetime import datetime, timedelta

# Create your models here.


items_days_limits = {
    "book": 30,
    "magazine": 7
}


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
        if self.item.item_type == "book":
            date_to_return = self.loaned_timestamp + \
                timedelta(days=items_days_limits['book'])
            days_left = (date_to_return - self.loaned_timestamp).days
        else:
            date_to_return = self.loaned_timestamp + \
                timedelta(days=items_days_limits['magazine'])
            days_left = (date_to_return - self.loaned_timestamp).days
        return days_left

    def is_available(self):
        # is not -> different than, aka -> !=
        # None is used to check if the value is NULL or not. You can't directly check on the value NULL using NULL.
        return self.returned_timestamp is not None
