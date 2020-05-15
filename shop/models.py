from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save


class Shop(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, default='', null=True)
    city = models.CharField(max_length=100, default='')
    shop_image = models.ImageField(
        null=True, blank=True, upload_to='documents/%Y/%m/%d/')
    date_created = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class MyModel(models.Model):
    upload = models.FileField(upload_to=user_directory_path)


def create_shop(sender, **kwargs):
    if kwargs['created']:
        shopo_profile = Shop.objects.create(user=kwargs['instance'])


post_save.connect(create_shop, sender=User)
