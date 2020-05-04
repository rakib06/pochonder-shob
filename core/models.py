from django.conf import settings
from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    pass

    def __str__(self):
        return self.title


class Order(models.Model):
    pass

    def __str__(self):
        return self.title
