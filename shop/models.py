from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save


class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, default='', null=True)
    city = models.CharField(max_length=100, default='')
    shop_image = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


def create_shop(sender, **kwargs):
    if kwargs['created']:
        shopo_profile = Shop.objects.create(user=kwargs['instance'])


post_save.connect(create_shop, sender=User)
