from django.conf import settings
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


COLOR_CHOICES = (
    ('BL', 'Black'),
    ('WT', 'White'),
    ('RD', 'Red')

)

LABEL_CHOICES = (

    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')

)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    color = models.CharField(choices=COLOR_CHOICES,
                             max_length=4, null=True)
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=1, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.title
